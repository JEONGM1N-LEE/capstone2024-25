export const uploadImage = async (imageFile: File) => {
    const formData = new FormData();
    formData.append('file', imageFile);

    const response = await fetch('http://localhost:8000/ocr/', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error('🚨 FastAPI OCR 요청 실패');
    }

    return await response.json();
};
