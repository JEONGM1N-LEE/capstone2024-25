import { json, type RequestHandler } from '@sveltejs/kit';

export const POST: RequestHandler = async ({ request }) => {
	const { message } = await request.json();

	const res = await fetch('https://api.openai.com/v1/chat/completions', {
		method: 'POST',
		headers: {
			Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			model: 'gpt-4o-mini',
			messages: [
				{ role: 'system', content: '너는 식품 영양분 전문가야. 성분표나 건강 관련 질문에 쉽게 대답해줘.' },
				{ role: 'user', content: message }
			],
			max_tokens: 1000
		})
	});

	const result = await res.json();
	return json({ result });
};
