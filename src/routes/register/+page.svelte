<script lang="ts">
	let name = '';
	let email = '';
	let password = '';
	let message = '';

	async function register() {
		const res = await fetch('/api/register', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, email, password })
		});
		const data = await res.json();
		message = data.message || data.error;

		if (res.ok) {
			window.location.href = '/login'; // 가입 후 로그인 페이지로 이동
		}
	}

	function goToLogin() {
		window.location.href = '/login';
	}
</script>

<style>
	/* ✅ 전체 화면 중앙 정렬 */
	.container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	/* ✅ 회원가입 박스 */
	.register-box {
		text-align: center;
	}

	form {
		display: flex;
		flex-direction: column;
		width: 300px;
		margin-top: 2rem;
	}

	input {
		margin-bottom: 1rem;
		padding: 0.5rem;
		border: none;
		border-bottom: 2px solid #ccc;
		outline: none;
		font-size: 1rem;
	}

	input:focus {
		border-bottom-color: #333;
	}

	button {
		padding: 0.5rem;
		font-size: 1rem;
		cursor: pointer;
		margin-top: 0.5rem;
	}
</style>

<!-- ✅ 전체 감싸는 중앙 정렬 컨테이너 -->
<div class="container">
	<div class="register-box">
		<h1>회원가입</h1>

		<form on:submit|preventDefault={register}>
			<input type="text" bind:value={name} placeholder="이름" required />
			<input type="email" bind:value={email} placeholder="이메일" required />
			<input type="password" bind:value={password} placeholder="비밀번호" required />
			<button type="submit">회원가입</button>
		</form>

		{#if message}
			<p>{message}</p>
		{/if}

		<p style="margin-top: 1.5rem;">이미 계정이 있으신가요?</p>
		<button on:click={goToLogin}>로그인</button>
	</div>
</div>