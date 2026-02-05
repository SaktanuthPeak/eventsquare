import QRCode from 'qrcode';

/**
 * Generate QR code as data URL
 * @param text - Text/data to encode in QR code (typically ticket ID)
 * @returns Promise<string> - Data URL of the QR code image
 */
export async function generateQRCode(text: string): Promise<string> {
	try {
		const qrCodeDataUrl = await QRCode.toDataURL(text, {
			errorCorrectionLevel: 'H',
			type: 'image/png',
			quality: 0.95,
			margin: 1,
			width: 300,
			color: {
				dark: '#000000',
				light: '#ffffff'
			}
		});
		return qrCodeDataUrl;
	} catch (err) {
		console.error('Error generating QR code:', err);
		throw new Error('Failed to generate QR code');
	}
}

/**
 * Generate QR code as Canvas element
 * @param text - Text/data to encode in QR code
 * @param canvas - Canvas element to render QR code to
 */
export async function generateQRCodeToCanvas(text: string, canvas: HTMLCanvasElement): Promise<void> {
	try {
		await QRCode.toCanvas(canvas, text, {
			errorCorrectionLevel: 'H',
			type: 'image/png',
			quality: 0.95,
			margin: 1,
			width: 300,
			color: {
				dark: '#000000',
				light: '#ffffff'
			}
		});
	} catch (err) {
		console.error('Error generating QR code to canvas:', err);
		throw new Error('Failed to generate QR code');
	}
}
