// src/routes/scanner/+server.ts
import type { RequestHandler } from './$types';
import { json } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
    const formData = await request.formData();
    const file = formData.get('image') as File;

    if (!file) {
        return json({ error: '파일이 제공되지 않았습니다.' }, { status: 400 });
    }

    // FastAPI OCR 기능 호출
    const fastApiRes = await fetch('http://localhost:8000/ocr/', {
        method: 'POST',
        body: formData
    });

    if (!fastApiRes.ok) {
        return json({ error: 'FastAPI OCR 요청 실패' }, { status: 500 });
    }

    const result = await fastApiRes.json();
    return json(result);
};
