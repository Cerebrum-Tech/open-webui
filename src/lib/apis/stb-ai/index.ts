import { WEBUI_API_BASE_URL } from '$lib/constants';

/**
 * Authenticate user with STB-AI cookie
 * @returns User session data if successful
 */
export const stbAiAuthenticate = async () => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/auths/stb-ai/auth`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include' // Important: include cookies in request
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.error('STB-AI authentication error:', err);
			error = err.detail || 'STB-AI authentication failed';
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

/**
 * Check if STB-AI cookie is present and valid
 * @returns Authentication status and user info
 */
export const checkStbAiCookie = async () => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/auths/stb-ai/check`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		},
		credentials: 'include'
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.error('STB-AI check error:', err);
			error = err.detail || 'Failed to check STB-AI status';
			return null;
		});

	if (error) {
		// Return false status instead of throwing for check endpoint
		return {
			authenticated: false,
			message: error
		};
	}

	return res;
};

/**
 * Attempt automatic STB-AI authentication
 * This function checks for STB-AI cookie and automatically authenticates if present
 */
export const tryStbAiAutoAuth = async () => {
	try {
		// First check if STB-AI cookie is present
		const checkResult = await checkStbAiCookie();
		
		if (checkResult && checkResult.authenticated) {
			// Cookie is present and valid, authenticate
			const authResult = await stbAiAuthenticate();
			return {
				success: true,
				user: authResult
			};
		}
		
		return {
			success: false,
			message: checkResult?.message || 'No STB-AI authentication available'
		};
	} catch (error) {
		console.error('STB-AI auto-auth error:', error);
		return {
			success: false,
			message: error.message || 'Auto-authentication failed'
		};
	}
};

