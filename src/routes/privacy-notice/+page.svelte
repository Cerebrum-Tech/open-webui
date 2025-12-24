<script lang="ts">
	import { getContext } from 'svelte';
	import { WEBUI_BASE_URL } from '$lib/constants';
	import { WEBUI_NAME } from '$lib/stores';

	const i18n = getContext('i18n');

	// Privacy Notice content in Turkish (Aydınlatma Metni)
	const privacyNoticeContent = `
<div class="space-y-6">
	<div class="text-center space-y-2">
		<h1 class="text-2xl font-bold">T.C. SANAYİ VE TEKNOLOJİ BAKANLIĞI</h1>
		<h2 class="text-xl font-semibold">İNTRANET YAPAY ZEKA ASİSTANI PORTAL'İ</h2>
		<h3 class="text-xl font-semibold">AYDINLATMA METNİ</h3>
	</div>

	<div class="space-y-6">
		<div>
			<h4 class="text-lg font-semibold mb-3">Aydınlatma Metni</h4>
			<p class="leading-relaxed">
				Bu Aydınlatma Metni, 6698 sayılı Kişisel Verilerin Korunması Kanunu'nun ("KVK Kanunu") "Veri Sorumlusunun Aydınlatma Yükümlülüğü" kenar başlıklı 10 uncu maddesi uyarınca ve KVK Kanunu kapsamında veri sorumlusu olan T.C. Sanayi ve Teknoloji Bakanlığı (Bakanlık) tarafından, İntranet Yapay Zeka Asistanı Portalı (Portal) kullanıcılarına, kullanıcılara ait kişisel veriler hususunda bilgilendirme yapmak amacıyla hazırlanmıştır. KVK Kanunu uyarınca veri sorumlusu sıfatını haiz Bakanlığın merkez adresi "Mustafa Kemal Mahallesi Dumlupınar Bulvarı (Eskişehir Yolu 7.km) İsmail Karakaya Cad. (Eski 2151. Cadde) No:154/A 06530 Çankaya/ANKARA" dir.
			</p>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">Veri Sorumlusunun Kimliği</h4>
			<p class="leading-relaxed">
				Bu uygulamada işlenen kişisel verileriniz bakımından veri sorumlusu T.C. Sanayi ve Teknoloji Bakanlığı'dır.
			</p>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">Kişisel Verilerin İşlenme Amaçları</h4>
			<p class="leading-relaxed mb-4">Bu Portal'de aşağıda yer alan kişisel verileriniz şu amaçlarla işlenmektedir.</p>
			<ul class="list-disc list-inside space-y-3 ml-4">
				<li>
					<strong>Kimlik verisi:</strong> T.C. Kimlik numarası, adı ve soyadı bilgileriniz, kimliğinizin doğrulanması, erişim yetkilerinin yürütülmesi, iş faaliyetlerinin yürütülmesi, finans ve muhasebe işlerinin yürütülmesi, iş sürekliliğinin sağlanması faaliyetlerinin yürütülmesi ile yönetim faaliyetlerinin yürütülmesi amacıyla işlenebilmektedir.
				</li>
				<li>
					<strong>İletişim verisi:</strong> e-Posta adresi, telefon numarası ve faks numarası bilgileriniz iletişim faaliyetlerinin yürütülmesi, iş faaliyetlerinin yürütülmesi, finans ve muhasebe işlerinin yürütülmesi, iş sürekliliğinin sağlanması faaliyetlerinin yürütülmesi ile yönetim faaliyetlerinin yürütülmesi amacıyla işlenebilmektedir.
				</li>
				<li>
					<strong>İşlem güvenliği verisi:</strong> IP adresi, sisteme giriş tarihi, sisteme son giriş tarihi ve veri oluşturma tarihi bilgileriniz bilgi güvenliği süreçlerinin yürütülmesi, iş faaliyetlerinin yürütülmesi, finans ve muhasebe işlerinin yürütülmesi, iş sürekliliğinin sağlanması faaliyetlerinin yürütülmesi ile yönetim faaliyetlerinin yürütülmesi amacıyla işlenebilmektedir.
				</li>
			</ul>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">Kişisel Verilerin Aktarımı</h4>
			<p class="leading-relaxed">
				Portal'deki kişisel verileriniz KVK Kanunu'nun 28 inci maddesinin ilk fıkrasında yer alan muafiyet halleri saklı kalmak üzere, hiçbir şekilde üçüncü taraflarla paylaşılmamaktadır.
			</p>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">Kişisel Veri Toplamanın Yöntemi ve Hukuki Sebebi</h4>
			<p class="leading-relaxed">
				Kişisel verileriniz tamamen otomatik yollarla (bu uygulama aracılığı ile) elde edilmektedir. Kişisel verileriniz KVK Kanunu'nun 5 inci maddesinin ikinci fıkrası uyarınca; veri sorumlusunun hukuki yükümlülüğünü yerine getirmesi, bir sözleşmenin kurulması veya ifasıyla doğrudan doğruya ilgili olması ve veri sorumlusunun meşru menfaatleri için veri işlenmesinin zorunlu olması hukuki sebeplerine dayanılarak işlenmektedir.
			</p>
		</div>

		<div>
			<h4 class="text-lg font-semibold mb-3">İlgili Kişilerin Hakları ve Veri Sorumlusuna Başvuru</h4>
			<p class="leading-relaxed mb-4">
				Portal Kullanıcıları KVK Kanunu'nun 11 inci maddesinde düzenlenen haklarını, KVK Kanunu'nun 13 üncü maddesi ve Veri Sorumlusuna Başvuru Usul ve Esasları Hakkında Tebliğ hükümleri çerçevesinde Bakanlığa başvurmak suretiyle kullanabilir.
			</p>
			<p class="leading-relaxed">
				KVK Kanunu'nun 13 üncü maddesi uyarınca yapılacak yazılı başvurular <strong>"Mustafa Kemal Mahallesi Dumlupınar Bulvarı (Eskişehir Yolu 7.km) İsmail Karakaya Cad. (Eski 2151. Cadde) No:154/A 06530 Çankaya/ANKARA"</strong> adresine; Kayıtlı Elektronik Posta (KEP) ile yapılacak başvurular ise <strong>"sanayiveteknolojibakanligi@hs01.kep.tr"</strong> adresine iletilmelidir.
			</p>
		</div>
	</div>
</div>
	`;
</script>

<svelte:head>
	<title>{$i18n.t('Privacy Notice')} | {$WEBUI_NAME}</title>
</svelte:head>

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
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
					</svg>
					<h1 class="text-2xl font-bold text-white">
						{$i18n.t('Privacy Notice')}
					</h1>
				</div>
				<p class="text-blue-100 mt-2 text-sm">
					{$i18n.t('Information about personal data processing on the Portal')}
				</p>
			</div>

			<!-- Content -->
			<div class="p-6 sm:p-8 text-gray-700 dark:text-gray-300">
				{@html privacyNoticeContent}
			</div>

			<!-- Footer -->
			<div class="px-6 py-4 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700">
				<p class="text-sm text-gray-500 dark:text-gray-400 text-center">
					{$i18n.t('This notice is provided in accordance with Article 10 of Law No. 6698 on the Protection of Personal Data.')}
				</p>
			</div>
		</div>
	</main>
</div>

