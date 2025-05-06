<script lang="ts">
	let email = '';
	let password = '';
	let message = '';

	async function login() {
		const res = await fetch('/api/login', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password })
		});
		const data = await res.json();
		message = data.message || data.error;

		if (res.ok) {
			localStorage.setItem('user', JSON.stringify(data.user));
			window.location.href = '/scanner';
		}
	}

	function goToRegister() {
		window.location.href = '/register';
	}
</script>

<style>
/* ✅ 전체를 감싸는 중앙 정렬 */
.container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
}

/* ✅ 로그인 박스 내부 스타일 */
.login-box {
	text-align: center;
}

/* ✅ 폼 정렬 및 스타일 */
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

<!-- ✅ 전체 가운데 정렬 시작 -->
<div class="container">
	<div class="login-box">
		<h1>로그인</h1>

		<form on:submit|preventDefault={login}>
			<input type="email" bind:value={email} placeholder="이메일" required />
			<input type="password" bind:value={password} placeholder="비밀번호" required />
			<button type="submit">로그인</button>
		</form>

		{#if message}
			<p>{message}</p>
		{/if}

		<p style="margin-top: 1.5rem;">아직 계정이 없으신가요?</p>
		<button on:click={goToRegister}>회원가입</button>
	</div>
</div>
  