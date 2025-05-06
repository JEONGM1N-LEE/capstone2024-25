// OCR 데이터를 처리하는 API
import type { RequestHandler } from '@sveltejs/kit';
import { json } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
  const formData = await request.formData();
  const image = formData.get('image') as File;

  if (!image) {
    return json({ error: '🚨 파일이 제공되지 않았습니다.' }, { status: 400 });
  }

  // FastAPI OCR 엔드포인트 호출
  const fastApiRes = await fetch('http://localhost:8000/ocr/', {
    method: 'POST',
    body: formData
  });

  if (!fastApiRes.ok) {
    return json({ error: '🚨 FastAPI OCR 요청 실패' }, { status: 500 });
  }

  const result = await fastApiRes.json();
  return json(result);
};

