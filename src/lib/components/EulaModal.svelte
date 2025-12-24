<script lang="ts">
	import { createEventDispatcher, getContext, onMount, tick } from 'svelte';
	import { fade } from 'svelte/transition';
	import { flyAndScale } from '$lib/utils/transitions';
	import { acceptAgreement } from '$lib/apis/agreements';
	import { toast } from 'svelte-sonner';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import { WEBUI_BASE_URL } from '$lib/constants';

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let show = false;
	export let token = '';

	let loading = false;
	let scrolledToBottom = false;
	let contentElement: HTMLDivElement | null = null;

	const checkScroll = () => {
		if (contentElement) {
			const { scrollTop, scrollHeight, clientHeight } = contentElement;
			// Allow a margin of 50px to account for potential rounding issues
			const atBottom = scrollTop + clientHeight >= scrollHeight - 50;
			scrolledToBottom = atBottom;
			console.log('Scroll check:', { scrollTop, scrollHeight, clientHeight, atBottom });
		}
	};

	const handleAccept = async () => {
		if (!scrolledToBottom) {
			toast.error($i18n.t('Please read the entire agreement before accepting.'));
			return;
		}

		loading = true;
		try {
			const tkn = token || localStorage?.token;
			if (!tkn) {
				toast.error('Authentication token not found');
				loading = false;
				return;
			}
			const result = await acceptAgreement(tkn, true, false);
			if (result) {
				dispatch('accepted');
				show = false;
			} else {
				toast.error($i18n.t('Failed to accept agreement. Please try again.'));
			}
		} catch (error) {
			console.error('Error accepting agreement:', error);
			toast.error($i18n.t('Failed to accept agreement. Please try again.'));
		} finally {
			loading = false;
		}
	};

	const scrollToBottom = () => {
		if (contentElement) {
			contentElement.scrollTo({
				top: contentElement.scrollHeight,
				behavior: 'smooth'
			});
		}
	};

	$: if (show && contentElement) {
		// Reset scroll state when modal opens
		scrolledToBottom = false;
		tick().then(() => {
			checkScroll();
		});
	}
</script>

{#if show}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div
		class="fixed inset-0 bg-black/80 flex items-center justify-center p-4 overflow-hidden"
		style="z-index: 99999;"
		in:fade={{ duration: 150 }}
	>
		<div
			class="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-3xl flex flex-col overflow-hidden"
			style="max-height: 90vh;"
			in:flyAndScale
			on:mousedown={(e) => e.stopPropagation()}
		>
			<!-- Header - Fixed height -->
			<div class="shrink-0 p-5 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
				<div class="flex items-center justify-center gap-3">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
					<h2 class="text-xl font-bold text-gray-900 dark:text-white">
						{$i18n.t('Terms of Use Agreement')}
					</h2>
				</div>
				<p class="text-center text-sm text-gray-500 dark:text-gray-400 mt-2">
					{$i18n.t('Please read and accept the following agreement to continue.')}
				</p>
			</div>

			<!-- Content - Scrollable area with fixed height -->
			<div
				bind:this={contentElement}
				class="overflow-y-auto p-5 text-gray-700 dark:text-gray-300 text-sm"
				style="height: 400px; max-height: 45vh;"
				on:scroll={checkScroll}
			>
				<div class="space-y-5">
					<div class="text-center space-y-1">
						<h1 class="text-lg font-bold">T.C. SANAYİ VE TEKNOLOJİ BAKANLIĞI</h1>
						<h2 class="text-base font-semibold">İNTRANET YAPAY ZEKA ASİSTANI PORTALI</h2>
						<h3 class="text-base font-semibold">KULLANIM SÖZLEŞMESİ</h3>
					</div>

					<p class="leading-relaxed">
						<strong>"Kullanım Sözleşmesi"</strong> (Sözleşme) siz değerli kullanıcılarımıza sistemimizde yer alan hizmetlerin sağlanmasına ilişkin hükümleri düzenlemektedir. Lütfen İntranet Yapay Zeka Asistanı Portalı'na (Portal) dâhil olmadan önce kullanım sözleşmesini dikkatle okuyunuz.
					</p>

					<div class="space-y-3">
						<div>
							<h4 class="font-semibold mb-2">İntranet Yapay Zeka Asistanı Portalı</h4>
							<p class="leading-relaxed">
								Bakanlık personelinin iş süreçlerini hızlandırmaya, kurumsal bilgiye erişimi kolaylaştırmaya ve metin/veri analizi yapmasına yardımcı olan bir uygulamadır.
							</p>
						</div>

						<div>
							<h4 class="font-semibold mb-2">Sorumluluk</h4>
							<p class="leading-relaxed mb-2">
								Portal'a <a href="https://intranet.sanayi.gov.tr/" class="text-blue-500 underline" target="_blank" rel="noopener noreferrer">https://intranet.sanayi.gov.tr/</a> web sitesi aracılığıyla giriş sağlanır. Bu web sitesinde yer alan sistemlere erişim sağlayan kullanıcılar, kullanıcı adı ve şifre bilgilerini üçüncü kişiler ile hiçbir surette paylaşmaz. Kullanıcı bu bilgilerin gizliliğini ve güvenliğini sağlamaktan münhasıran sorumlu olup aksi durumda doğabilecek olumsuz sonuçlardan T.C. Sanayi ve Bakanlığının (Bakanlık) hukuki, idari ve cezai herhangi bir sorumluluğu olmadığını kabul, beyan ve taahhüt eder.
							</p>
							<p class="leading-relaxed mb-2">
								Bakanlık, kendi takdirinde olmak üzere portal içeriğini ve kullanıcılara sağlanan herhangi bir hizmeti dilediği zaman değiştirme, kısıtlama, sona erdirme ile uygulamada kayıtlı kullanıcı bilgi ve verilerini silme hakkını saklı tutar.
							</p>
							<p class="leading-relaxed mb-2">
								Bakanlık; portalın sağlıklı çalışmasını tehlikeye sokacak bir tehdit gördüğünde veya gerekli bakım ve güncelleme çalışmaları sırasında portalı geçici süre ile erişime kapatabilir. Ayrıca Bakanlık, Sözleşme'yi ihlal eden kullanıcıların giriş yetkilerini geçici veya sürekli olarak iptal etme hakkını saklı tutar.
							</p>
							<p class="leading-relaxed mb-2">
								Kullanıcı; Portal'ın kullanılması esnasında karşılaşılabilecek hata, eksiklik, bilgisayar sistemlerine zarar vermeye yönelik herhangi bir yazılım (virüs), kusur; yönetimsel, konuşlandırmadan kaynaklı gecikmelerden ve/veya sistem bağlantı arızası sonucu görülebilecek doğrudan ya da dolaylı ziyan, zarar veya masraflar da dahil ve ancak bunlarla sınırlı olmamak üzere hiçbir zarar ve ziyandan Bakanlık ve/veya çalışanlarının, bu tip olasılıklardan haberdar olsun ya da olmasın sorumlu tutulamayacağını kabul, beyan ve taahhüt eder.
							</p>
							<p class="leading-relaxed mb-2">
								Portal'de sunulan hizmet, uygulama ve sistemler açık kaynak kodlu yazılımlar veya Bakanlık tarafından sağlanan yazılımlardır. Bu yazılımlardaki hatalar ve eksikliklerde Bakanlığın sorumlu olmadığını ve <strong>bu yazılımların kullanımı sonrasında elde edilen bilgilerin yeterli, doğru ve eksiksiz olmayabileceğini kabul, beyan ve taahhüt eder.</strong>
							</p>
							<p class="leading-relaxed mb-2">
								Kullanıcı, Portal'i kullanırken mahremiyet hakkına riayet edilmesinin başta 6698 sayılı Kişisel Verilerin Korunması Kanunu'nda yer alan hükümlerden kaynaklanan hukuki bir yükümlülük ve aynı zamanda mesleki etik kuralı olduğunun bilinci ile Portal'i yalnızca mevzuat tarafından sınırları çizilen amaçlar için kullanacağını, bireysel hak ve menfaat temini amacıyla Portal'i kullanmayacağını, Kamu Görevlileri Etik Davranış İlkeleri çerçevesinde hareket edeceğini, aksi halde hakkında müeyyide uygulanabileceğini kabul, beyan ve taahhüt eder.
							</p>
							<p class="leading-relaxed font-semibold">
								Kullanıcı, Portal'de sunulan hizmet, uygulama ve sistemleri kullanırken Bakanlığa veya Bakanlık çalışanına ait kişisel veya kurumsal verileri kullanmayacağını aksi halde hakkında müeyyide uygulanabileceğini kabul, beyan ve taahhüt eder.
							</p>
						</div>

						<div>
							<h4 class="font-semibold mb-2">Uyuşmazlık</h4>
							<p class="leading-relaxed mb-2">
								Kullanıcı, Portal'e giriş yapmadan önce bu Sözleşme'yi okuyacağını, burada yer alan tüm hükümlere uyacağını, bu hükümlere ilişkin herhangi bir uyuşmazlık veya ihtilafın söz konusu olması hâlinde Ankara Mahkeme ve İcra Dairelerinin yetkili olacağını, Portal'de yer alan içeriklerin ve Bakanlığa ait tüm elektronik kayıtların 6100 sayılı Hukuk Muhakemeleri Kanunu'nun 193'üncü maddesinin birinci fıkrası uyarınca kesin delil sayılacağını kabul, beyan ve taahhüt eder.
							</p>
							<p class="leading-relaxed">
								Kullanıcı; Bakanlığın, Sözleşme'yi tek taraflı olarak her zaman değiştirme veya güncelleme hakkına sahip olduğunu, bunlarda yapılacak her türlü değişikliği peşinen kabul ettiğini beyan eder.
							</p>
						</div>
					</div>

					<!-- End marker to help users know they've reached the end -->
					<div class="text-center pt-4 pb-2 border-t border-gray-200 dark:border-gray-700">
						<p class="text-xs text-gray-400 dark:text-gray-500">— Sözleşme Sonu —</p>
					</div>
				</div>
			</div>

			<!-- Scroll indicator / helper -->
			{#if !scrolledToBottom}
				<div class="shrink-0 px-5 py-2 bg-amber-50 dark:bg-amber-900/30 border-t border-amber-200 dark:border-amber-800">
					<button 
						class="w-full text-sm text-amber-700 dark:text-amber-300 text-center flex items-center justify-center gap-2 hover:underline"
						on:click={scrollToBottom}
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
						</svg>
						{$i18n.t('Please scroll down to read the entire agreement')}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
						</svg>
					</button>
				</div>
			{/if}

			<!-- Footer - Fixed height -->
			<div class="shrink-0 p-5 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
				<button
					class="w-full py-3 px-6 rounded-xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 {scrolledToBottom 
						? 'bg-blue-600 hover:bg-blue-700 cursor-pointer shadow-lg hover:shadow-xl' 
						: 'bg-gray-400 dark:bg-gray-600 cursor-not-allowed opacity-60'}"
					on:click={handleAccept}
					disabled={loading || !scrolledToBottom}
				>
					{#if loading}
						<Spinner className="w-5 h-5" />
						{$i18n.t('Processing...')}
					{:else}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
						</svg>
						{$i18n.t('I have read and accept the Terms of Use')}
					{/if}
				</button>
				
				<!-- Privacy Notice Link -->
				<p class="text-center text-xs text-gray-600 dark:text-gray-400 mt-3">
					{$i18n.t('Additionally, you can access the Privacy Notice')}
					<a 
						href="{WEBUI_BASE_URL}/privacy-notice" 
						target="_blank"
						rel="noopener noreferrer"
						class="text-blue-600 dark:text-blue-400 hover:underline font-medium"
					>
						{$i18n.t('here')}
					</a>
					{$i18n.t('to obtain detailed information regarding your personal data processed on the Portal.')}
				</p>
			</div>
		</div>
	</div>
{/if}
