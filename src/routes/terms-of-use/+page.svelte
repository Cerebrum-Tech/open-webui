<script lang="ts">
	import { getContext } from 'svelte';
	import { WEBUI_BASE_URL } from '$lib/constants';
	import { WEBUI_NAME, user } from '$lib/stores';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	const i18n = getContext('i18n');

	onMount(() => {
		// Redirect to auth if not logged in
		if (!$user) {
			goto('/auth');
		}
	});

	// Terms of Use content in Turkish (Kullanım Sözleşmesi)
	const termsOfUseContent = `
<div class="space-y-6">
	<div class="text-center space-y-2">
		<h1 class="text-2xl font-bold">T.C. SANAYİ VE TEKNOLOJİ BAKANLIĞI</h1>
		<h2 class="text-xl font-semibold">İNTRANET YAPAY ZEKA ASİSTANI PORTALI</h2>
		<h3 class="text-xl font-semibold">KULLANIM SÖZLEŞMESİ</h3>
	</div>

	<p class="leading-relaxed">
		<strong>"Kullanım Sözleşmesi"</strong> (Sözleşme) siz değerli kullanıcılarımıza sistemimizde yer alan hizmetlerin sağlanmasına ilişkin hükümleri düzenlemektedir. Lütfen İntranet Yapay Zeka Asistanı Portalı'na (Portal) dâhil olmadan önce kullanım sözleşmesini dikkatle okuyunuz.
	</p>

	<div class="space-y-6">
		<div>
			<h4 class="text-lg font-semibold mb-3">İntranet Yapay Zeka Asistanı Portalı</h4>
			<p class="leading-relaxed">
				Bakanlık personelinin iş süreçlerini hızlandırmaya, kurumsal bilgiye erişimi kolaylaştırmaya ve metin/veri analizi yapmasına yardımcı olan bir uygulamadır.
			</p>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">Sorumluluk</h4>
			<p class="leading-relaxed mb-4">
				Portal'a <a href="https://intranet.sanayi.gov.tr/" class="text-blue-500 underline" target="_blank">https://intranet.sanayi.gov.tr/</a> web sitesi aracılığıyla giriş sağlanır. Bu web sitesinde yer alan sistemlere erişim sağlayan kullanıcılar, kullanıcı adı ve şifre bilgilerini üçüncü kişiler ile hiçbir surette paylaşmaz. Kullanıcı bu bilgilerin gizliliğini ve güvenliğini sağlamaktan münhasıran sorumlu olup aksi durumda doğabilecek olumsuz sonuçlardan T.C. Sanayi ve Bakanlığının (Bakanlık) hukuki, idari ve cezai herhangi bir sorumluluğu olmadığını kabul, beyan ve taahhüt eder.
			</p>
			<p class="leading-relaxed mb-4">
				Bakanlık, kendi takdirinde olmak üzere portal içeriğini ve kullanıcılara sağlanan herhangi bir hizmeti dilediği zaman değiştirme, kısıtlama, sona erdirme ile uygulamada kayıtlı kullanıcı bilgi ve verilerini silme hakkını saklı tutar.
			</p>
			<p class="leading-relaxed mb-4">
				Bakanlık; portalın sağlıklı çalışmasını tehlikeye sokacak bir tehdit gördüğünde veya gerekli bakım ve güncelleme çalışmaları sırasında portalı geçici süre ile erişime kapatabilir. Ayrıca Bakanlık, Sözleşme'yi ihlal eden kullanıcıların giriş yetkilerini geçici veya sürekli olarak iptal etme hakkını saklı tutar.
			</p>
			<p class="leading-relaxed mb-4">
				Kullanıcı; Portal'ın kullanılması esnasında karşılaşılabilecek hata, eksiklik, bilgisayar sistemlerine zarar vermeye yönelik herhangi bir yazılım (virüs), kusur; yönetimsel, konuşlandırmadan kaynaklı gecikmelerden ve/veya sistem bağlantı arızası sonucu görülebilecek doğrudan ya da dolaylı ziyan, zarar veya masraflar da dahil ve ancak bunlarla sınırlı olmamak üzere hiçbir zarar ve ziyandan Bakanlık ve/veya çalışanlarının, bu tip olasılıklardan haberdar olsun ya da olmasın sorumlu tutulamayacağını kabul, beyan ve taahhüt eder.
			</p>
			<p class="leading-relaxed mb-4">
				Portal'de sunulan hizmet, uygulama ve sistemler açık kaynak kodlu yazılımlar veya Bakanlık tarafından sağlanan yazılımlardır. Bu yazılımlardaki hatalar ve eksikliklerde Bakanlığın sorumlu olmadığını ve <strong>bu yazılımların kullanımı sonrasında elde edilen bilgilerin yeterli, doğru ve eksiksiz olmayabileceğini kabul, beyan ve taahhüt eder.</strong>
			</p>
			<p class="leading-relaxed mb-4">
				Kullanıcı, Portal'i kullanırken mahremiyet hakkına riayet edilmesinin başta 6698 sayılı Kişisel Verilerin Korunması Kanunu'nda yer alan hükümlerden kaynaklanan hukuki bir yükümlülük ve aynı zamanda mesleki etik kuralı olduğunun bilinci ile Portal'i yalnızca mevzuat tarafından sınırları çizilen amaçlar için kullanacağını, bireysel hak ve menfaat temini amacıyla Portal'i kullanmayacağını, Kamu Görevlileri Etik Davranış İlkeleri çerçevesinde hareket edeceğini, aksi halde hakkında müeyyide uygulanabileceğini kabul, beyan ve taahhüt eder.
			</p>
			<p class="leading-relaxed font-semibold">
				Kullanıcı, Portal'de sunulan hizmet, uygulama ve sistemleri kullanırken Bakanlığa veya Bakanlık çalışanına ait kişisel veya kurumsal verileri kullanmayacağını aksi halde hakkında müeyyide uygulanabileceğini kabul, beyan ve taahhüt eder.
			</p>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">Uyuşmazlık</h4>
			<p class="leading-relaxed mb-4">
				Kullanıcı, Portal'e giriş yapmadan önce bu Sözleşme'yi okuyacağını, burada yer alan tüm hükümlere uyacağını, bu hükümlere ilişkin herhangi bir uyuşmazlık veya ihtilafın söz konusu olması hâlinde Ankara Mahkeme ve İcra Dairelerinin yetkili olacağını, Portal'de yer alan içeriklerin ve Bakanlığa ait tüm elektronik kayıtların 6100 sayılı Hukuk Muhakemeleri Kanunu'nun 193'üncü maddesinin birinci fıkrası uyarınca kesin delil sayılacağını kabul, beyan ve taahhüt eder.
			</p>
			<p class="leading-relaxed">
				Kullanıcı; Bakanlığın, Sözleşme'yi tek taraflı olarak her zaman değiştirme veya güncelleme hakkına sahip olduğunu, bunlarda yapılacak her türlü değişikliği peşinen kabul ettiğini beyan eder.
			</p>
		</div>
	</div>
</div>
	`;
</script>

<svelte:head>
	<title>{$i18n.t('Terms of Use')} | {$WEBUI_NAME}</title>
</svelte:head>

{#if $user}
<div class="fixed inset-0 bg-gray-50 dark:bg-gray-950 overflow-y-auto">
	<!-- Header -->
	<header class="sticky top-0 z-10 bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-800">
		<div class="max-w-4xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
			<div class="flex items-center justify-between">
				<a href="/" class="flex items-center gap-3 text-gray-900 dark:text-white hover:opacity-80 transition-opacity">
					<img
						crossorigin="anonymous"
						src="{WEBUI_BASE_URL}/static/favicon.png"
						class="w-8 h-8"
						alt="logo"
					/>
					<span class="font-semibold text-lg">{$WEBUI_NAME}</span>
				</a>
				<a 
					href="/"
					class="text-sm text-blue-600 dark:text-blue-400 hover:underline"
				>
					← {$i18n.t('Back to Portal')}
				</a>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8 pb-16">
		<div class="bg-white dark:bg-gray-900 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
			<!-- Title Bar -->
			<div class="bg-blue-600 dark:bg-blue-700 px-6 py-4">
				<div class="flex items-center gap-3">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
					<h1 class="text-2xl font-bold text-white">
						{$i18n.t('Terms of Use')}
					</h1>
				</div>
				<p class="text-blue-100 mt-2 text-sm">
					{$i18n.t('User agreement for the Intranet AI Assistant Portal')}
				</p>
			</div>

			<!-- Content -->
			<div class="p-6 sm:p-8 text-gray-700 dark:text-gray-300">
				{@html termsOfUseContent}
			</div>

			<!-- Footer with Privacy Notice Link -->
			<div class="px-6 py-4 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700">
				<p class="text-sm text-gray-600 dark:text-gray-400 text-center">
					{$i18n.t('Additionally, you can access the Privacy Notice')}
					<a 
						href="/privacy-notice" 
						class="text-blue-600 dark:text-blue-400 hover:underline font-medium"
					>
						{$i18n.t('here')}
					</a>
					{$i18n.t('to obtain detailed information regarding your personal data processed on the Portal.')}
				</p>
			</div>
		</div>
	</main>
</div>
{/if}

