import prisma from '$lib/prisma';
import bcrypt from 'bcrypt';
import type { RequestEvent } from '@sveltejs/kit';

export async function POST({ request }: RequestEvent) {
	const { email, password } = await request.json();

	const user = await prisma.user.findUnique({ where: { email } });
	if (!user || !(await bcrypt.compare(password, user.password))) {
		return new Response(JSON.stringify({ error: '이메일 또는 비밀번호가 틀렸습니다.' }), { status: 401 });
	}

	// 비밀번호 제거
	const { password: _, ...userSafe } = user;

	return new Response(JSON.stringify({ message: '로그인 성공!', user: userSafe }), {
		status: 200
	});
}