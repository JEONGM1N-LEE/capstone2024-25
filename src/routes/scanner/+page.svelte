<script lang="ts">
    import { uploadImage } from '../../lib/api';

    let imageFile: File | null = null;
    let previewUrl: string | null = null;
    let messages: { role: 'user' | 'assistant'; text: string }[] = [];
    let userInput = '';

    // 이미지 선택 시 실행
    async function handleImageUpload(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target.files && target.files.length > 0) {
            imageFile = target.files[0];
            previewUrl = URL.createObjectURL(imageFile);

            messages = [...messages, { role: 'user', text: '📷 영양성분표 사진을 업로드했어요.' }];
            await analyzeImage();
        }
    }

    // FastAPI OCR 분석 및 알러지 감지
    async function analyzeImage() {
    if (!imageFile) return;

    try {
        console.log("🚀 FastAPI OCR 요청 시작...");
        const response = await uploadImage(imageFile);
        console.log("✅ FastAPI 응답:", response);

        // 응답이 객체 형태이므로, 텍스트를 정확히 추출하여 표시
        // const warningMessage = response.warning ? response.warning : JSON.stringify(response);

		// JSON 객체에서 "warning" 메시지만 추출하여 UI에 표시
        const warningMessage = response.warning ?? "✅ 안전합니다!";

        messages = [...messages, { role: 'assistant', text: warningMessage }];
    } catch (error) {
        console.error("🚨 OCR 요청 실패:", error);
        messages = [...messages, { role: 'assistant', text: "🚨 오류 발생! 다시 시도해 주세요." }];
   		}
	}
	

    // 사용자 질문 전송
    async function sendMessage() {
        if (!userInput.trim()) return;

        messages = [...messages, { role: 'user', text: userInput }];

        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        const data = await res.json();
        const reply = data.result?.choices?.[0]?.message?.content || 'AI 응답을 불러오지 못했습니다.';
        messages = [...messages, { role: 'assistant', text: reply }];
        userInput = '';
    }
</script>

<style>
	.chat {
		max-width: 600px;
		margin: 2rem auto;
		padding: 1.5rem;
		border: 1px solid #ddd;
		border-radius: 10px;
		background: #f9f9f9;
	}

	.message {
		margin: 1rem 0;
	}

	.message.user {
		text-align: right;
	}

	.message.assistant {
		text-align: left;
		color: #333;
	}

	input[type="file"] {
		margin-bottom: 1rem;
	}

	.input-row {
		margin-top: 2rem;
		display: flex;
		gap: 0.5rem;
	}

	input[type="text"] {
		flex: 1;
		padding: 0.5rem;
		font-size: 1rem;
	}
</style>

<div class="chat">
	<h2>🍥 AI 성분 분석 챗봇</h2>

	<!-- 📷 이미지 업로드 -->
	<input type="file" accept="image/*" on:change={handleImageUpload} />

	<!-- 미리보기 이미지 -->
	{#if previewUrl}
		<img src={previewUrl} alt="미리보기" style="max-width: 200px; margin-bottom: 1rem;" />
	{/if}

	<!-- 💬 메시지 출력 -->
	{#each messages as msg}
		<div class="message {msg.role}">
			<p><strong>{msg.role === 'user' ? '🙋 나' : '🤖 AI'}:</strong> {msg.text}</p>
		</div>
	{/each}

	<!-- 🧑 사용자 질문 입력 -->
	<div class="input-row">
		<input
			type="text"
			bind:value={userInput}
			placeholder="질문을 입력하세요..."
			on:keydown={(e) => e.key === 'Enter' && sendMessage()}
		/>
		<button on:click={sendMessage}>전송</button>
	</div>
</div>
  
  