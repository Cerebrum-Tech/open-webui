<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { getAgreementsReport, resetOwnAgreement } from '$lib/apis/agreements';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import { toast } from 'svelte-sonner';

	const i18n = getContext('i18n');

	let loading = true;
	let resetting = false;
	let report: any = null;
	let filter = 'all'; // 'all', 'accepted', 'pending'
	let searchQuery = '';

	const loadReport = async () => {
		loading = true;
		try {
			report = await getAgreementsReport(localStorage.token);
		} catch (error) {
			console.error('Error loading agreements report:', error);
			toast.error($i18n.t('Failed to load agreements report'));
		} finally {
			loading = false;
		}
	};

	const handleResetOwnEula = async () => {
		if (!confirm($i18n.t('Are you sure you want to reset your own EULA acceptance? You will see the EULA modal again after refreshing the page.'))) {
			return;
		}
		
		resetting = true;
		try {
			const result = await resetOwnAgreement(localStorage.token);
			if (result) {
				toast.success($i18n.t('Your EULA acceptance has been reset. Refresh the page to see the modal.'));
				await loadReport();
			}
		} catch (error) {
			console.error('Error resetting agreement:', error);
			toast.error($i18n.t('Failed to reset agreement'));
		} finally {
			resetting = false;
		}
	};

	const formatDate = (timestamp: number | null) => {
		if (!timestamp) return '-';
		return new Date(timestamp * 1000).toLocaleString('tr-TR', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit'
		});
	};

	$: filteredAgreements = report?.agreements?.filter((a: any) => {
		// Filter by status
		if (filter === 'accepted' && !a.eula_accepted) return false;
		if (filter === 'pending' && a.eula_accepted) return false;
		
		// Filter by search
		if (searchQuery) {
			const query = searchQuery.toLowerCase();
			return (
				a.user_name?.toLowerCase().includes(query) ||
				a.user_email?.toLowerCase().includes(query)
			);
		}
		return true;
	}) || [];

	const exportToCSV = () => {
		if (!report?.agreements) return;
		
		const headers = ['User Name', 'Email', 'EULA Accepted', 'Acceptance Date'];
		const rows = report.agreements.map((a: any) => [
			a.user_name || '',
			a.user_email || '',
			a.eula_accepted ? 'Yes' : 'No',
			formatDate(a.eula_accepted_at)
		]);
		
		const csvContent = [
			headers.join(','),
			...rows.map((row: string[]) => row.map(cell => `"${cell}"`).join(','))
		].join('\n');
		
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
		const link = document.createElement('a');
		link.href = URL.createObjectURL(blob);
		link.download = `eula-agreements-report-${new Date().toISOString().split('T')[0]}.csv`;
		link.click();
	};

	onMount(() => {
		loadReport();
	});
</script>

<div class="py-4">
	<div class="mb-6 flex justify-between items-start">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
				{$i18n.t('EULA Agreements Report')}
			</h1>
			<p class="text-sm text-gray-500 dark:text-gray-400">
				{$i18n.t('View and manage user agreement acceptances')}
			</p>
		</div>
		<button
			class="px-4 py-2 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 hover:bg-red-200 dark:hover:bg-red-900/50 text-sm font-medium flex items-center gap-2 disabled:opacity-50"
			on:click={handleResetOwnEula}
			disabled={resetting}
		>
			{#if resetting}
				<Spinner className="w-4 h-4" />
			{:else}
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
				</svg>
			{/if}
			{$i18n.t('Reset My EULA (Test)')}
		</button>
	</div>

	{#if loading}
		<div class="flex justify-center items-center py-20">
			<Spinner className="w-8 h-8" />
		</div>
	{:else if report}
		<!-- Stats Cards -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
			<div class="bg-white dark:bg-gray-900 rounded-xl p-4 border border-gray-200 dark:border-gray-800">
				<div class="text-sm text-gray-500 dark:text-gray-400">{$i18n.t('Total Users')}</div>
				<div class="text-3xl font-bold text-gray-900 dark:text-white">{report.total}</div>
			</div>
			<div class="bg-white dark:bg-gray-900 rounded-xl p-4 border border-green-200 dark:border-green-800">
				<div class="text-sm text-green-600 dark:text-green-400">{$i18n.t('Accepted')}</div>
				<div class="text-3xl font-bold text-green-600 dark:text-green-400">{report.accepted_count}</div>
			</div>
			<div class="bg-white dark:bg-gray-900 rounded-xl p-4 border border-amber-200 dark:border-amber-800">
				<div class="text-sm text-amber-600 dark:text-amber-400">{$i18n.t('Pending')}</div>
				<div class="text-3xl font-bold text-amber-600 dark:text-amber-400">{report.pending_count}</div>
			</div>
		</div>

		<!-- Filters and Search -->
		<div class="flex flex-col sm:flex-row gap-4 mb-4">
			<div class="flex gap-2">
				<button
					class="px-4 py-2 rounded-lg text-sm font-medium transition-colors {filter === 'all' 
						? 'bg-blue-600 text-white' 
						: 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'}"
					on:click={() => filter = 'all'}
				>
					{$i18n.t('All')} ({report.total})
				</button>
				<button
					class="px-4 py-2 rounded-lg text-sm font-medium transition-colors {filter === 'accepted' 
						? 'bg-green-600 text-white' 
						: 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'}"
					on:click={() => filter = 'accepted'}
				>
					{$i18n.t('Accepted')} ({report.accepted_count})
				</button>
				<button
					class="px-4 py-2 rounded-lg text-sm font-medium transition-colors {filter === 'pending' 
						? 'bg-amber-600 text-white' 
						: 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'}"
					on:click={() => filter = 'pending'}
				>
					{$i18n.t('Pending')} ({report.pending_count})
				</button>
			</div>
			
			<div class="flex-1">
				<input
					type="text"
					placeholder={$i18n.t('Search by name or email...')}
					bind:value={searchQuery}
					class="w-full px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400"
				/>
			</div>
			
			<button
				class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 text-sm font-medium flex items-center gap-2"
				on:click={exportToCSV}
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
				</svg>
				{$i18n.t('Export CSV')}
			</button>
			
			<button
				class="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 text-sm font-medium flex items-center gap-2"
				on:click={loadReport}
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
				</svg>
				{$i18n.t('Refresh')}
			</button>
		</div>

		<!-- Table -->
		<div class="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-gray-50 dark:bg-gray-800">
						<tr>
							<th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
								{$i18n.t('User')}
							</th>
							<th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
								{$i18n.t('Email')}
							</th>
							<th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
								{$i18n.t('Status')}
							</th>
							<th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
								{$i18n.t('Acceptance Date')}
							</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 dark:divide-gray-700">
						{#each filteredAgreements as agreement}
							<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
								<td class="px-4 py-3 whitespace-nowrap">
									<div class="text-sm font-medium text-gray-900 dark:text-white">
										{agreement.user_name || '-'}
									</div>
								</td>
								<td class="px-4 py-3 whitespace-nowrap">
									<div class="text-sm text-gray-500 dark:text-gray-400">
										{agreement.user_email || '-'}
									</div>
								</td>
								<td class="px-4 py-3 whitespace-nowrap text-center">
									{#if agreement.eula_accepted}
										<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300">
											<svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
												<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
											</svg>
											{$i18n.t('Accepted')}
										</span>
									{:else}
										<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300">
											<svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
												<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
											</svg>
											{$i18n.t('Pending')}
										</span>
									{/if}
								</td>
								<td class="px-4 py-3 whitespace-nowrap">
									<div class="text-sm text-gray-500 dark:text-gray-400">
										{formatDate(agreement.eula_accepted_at)}
									</div>
								</td>
							</tr>
						{:else}
							<tr>
								<td colspan="4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
									{$i18n.t('No users found')}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>

		<!-- Summary -->
		<div class="mt-4 text-sm text-gray-500 dark:text-gray-400 text-right">
			{$i18n.t('Showing')} {filteredAgreements.length} {$i18n.t('of')} {report.total} {$i18n.t('users')}
		</div>
	{:else}
		<div class="text-center py-20 text-gray-500 dark:text-gray-400">
			{$i18n.t('Failed to load report')}
		</div>
	{/if}
</div>

