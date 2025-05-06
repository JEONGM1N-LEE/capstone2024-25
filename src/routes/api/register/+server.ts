import prisma from '$lib/prisma';
import bcrypt from 'bcrypt';
import type { RequestEvent } from '@sveltejs/kit';

export async function POST({ request }: RequestEvent) {
	const { name, email, password } = await request.json();

	// 이메일 중복 검사
	const existingUser = await prisma.user.findUnique({ where: { email } });
	if (existingUser) {
		return new Response(JSON.stringify({ error: '이미 가입된 이메일입니다.' }), { status: 400 });
	}

	// 비밀번호 해싱
	const hashedPassword = await bcrypt.hash(password, 10);

	// 사용자 저장
	const newUser = await prisma.user.create({
		data: { name, email, password: hashedPassword }
	});

	// 비밀번호 제거 후 응답
	const { password: _, ...userSafe } = newUser;

	return new Response(JSON.stringify({ message: '회원가입 완료!', user: userSafe }), {
		status: 201
	});
}