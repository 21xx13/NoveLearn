async function checkSlides(id) {
    if (id !== 'None') {
        let response = await fetch('/users/' + id, {
            method: 'GET'
        });
        let answer = await response.json();
        let responseSlide = await fetch('/slides/' + answer.slides, {
            method: 'GET'
        });
        let answerSlide = await responseSlide.json();
        let responseTest = await fetch('/testslide/' + answer.task_slides, {
            method: 'GET'
        });
        let answerTest = await responseTest.json();
        let slideCountResp = await fetch('/courseslides/', {
            method: 'GET'
        });
        let slideCount = await slideCountResp.json();
        let slideElems = document.querySelectorAll('.slide-check');
        let taskElems = document.querySelectorAll('.slide-check-test');
        slideElems.forEach(elem => {
            if (answerSlide.read_slides.includes(+elem.id)) {
                elem.innerHTML = "<span><i class=\"fa fa-check-square-o\" aria-hidden=\"true\"></i></span>"
            }
        });

        taskElems.forEach(elem => {
            if (answerTest.done_tests.includes(+elem.id)) {
                elem.innerHTML = "<span><i class=\"fa fa-check-square-o\" aria-hidden=\"true\"></i></span>"
            }
        });

        let questResp = await fetch('/questions/', {
            method: 'GET'
        });
        let scoreResp = await fetch('/scores/' + answer.score, {
            method: 'GET'
        });
        let score = await scoreResp.json();
        let questions = await questResp.json();
        let taskPointsAll = questions.map(el => el.weight).reduce((a, b) => a + b, 0);
        document.getElementById('task-done').innerText = score.score;
        document.getElementById('task-all').innerText = taskPointsAll;
        document.getElementById('slide-read').innerText = answerSlide.read_slides.length;
        document.getElementById('slide-all').innerText = slideCount.length;
        let lecturePercent = (answerSlide.read_slides.length / slideCount.length) * 0.5;
        let result = Math.round((lecturePercent + (score.score / taskPointsAll * 0.5)) * 100);
        if (result > 6) {
            document.getElementById('progress-perc').style.display = 'None';
            document.getElementById('progress').innerText = `${result}%`;
            document.getElementById('progress').style.width = `${result}%`
        } else {
            document.getElementById('progress-perc').innerText = result > 4 ? '' : `${result}%`;
            document.getElementById('progress').style.width = result < 5 && result > 0 ? '2%' : `${result}%`;
        }
    }
}