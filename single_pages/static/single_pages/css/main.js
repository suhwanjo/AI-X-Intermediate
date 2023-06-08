const progress = document.getElementById('progress')
const prev = document.getElementById('prev')
const next = document.getElementById('next')
const circles = document.querySelectorAll('.circle')
const text = document.getElementById('text')

//1,2,3단계 표시
let currentActive = 0

//단계 설명 리스트
list = ['1단계 순화: 욕설과 비속어를 @@로 변경','2단계 순화: @@을 적절한 단어로 순화','3단계 순화: 공격적인 표현 제거']

// 다음 버튼 클릭시
next.addEventListener('click', () => {
    if (currentActive < circles.length - 1) {
        text.textContent = list[currentActive];
        currentActive++;
        prev.disabled = false;
    }

    if (currentActive >= circles.length - 1) {
        currentActive = circles.length - 1;
        next.disabled = true;
    }
    update();
});

// 이전 버튼 클릭시
prev.addEventListener('click', () => {
    if (currentActive > 0) {
        currentActive--;
        text.textContent = list[currentActive-1];
        next.disabled = false;
    }

    if (currentActive <= 0) {
        currentActive = 0;
        prev.disabled = true;
        text.textContent = '';
    }
    update();
});

function update() {
    circles.forEach((circle, idx) => {
        if(idx < currentActive) {
            circle.classList.add('active')
        } else {
            circle.classList.remove('active')
        }
    })

    const actives = document.querySelectorAll('.active')

    progress.style.width = (actives.length - 1) / (circles.length - 1) * 100 + '%'

    if(currentActive === 0) {
        prev.disabled = true
    } else if(currentActive === 3) {
        next.disabled = true
    } else {
        prev.disabled = false
        next.disabled = false
    }
}