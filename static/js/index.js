window.onload = function () {

    let img = document.querySelectorAll('#theme-slides .theme-slide');
    let index = 0;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function addUserSlide() {
        let userId = document.getElementById('user-id').innerHTML;
        if (window.location.href.includes('/course/')
            && window.location.href !== 'http://127.0.0.1:8000/course/' && userId !== "None") {
            let slideCode = window.location.href.split('/course/')[1]
            const csrftoken = getCookie('csrftoken');
            console.log(csrftoken);
            fetch('/add_slide/', {
                method: 'POST',
                headers: {
                    "X-CSRFToken": csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    slideCode: slideCode,
                })
            }).then(response => {
                if (response.ok) {
                    return response.json()
                } else {
                    return Promise.reject(response)
                }
            }).then(data => {
                console.log('Слайд добавлен');
            }).catch(err => console.log(err))
        }
        checkSlides(userId);
    }

    async function renderUserAnswers() {
        let userId = +document.getElementById('user-id').innerHTML;
        if (window.location.href.includes('/course/')
            && window.location.href !== 'http://127.0.0.1:8000/course/' && userId !== "None") {
            if (document.querySelectorAll('.form-test').length > 0) {
                let codesList = [];
                document.querySelectorAll('.quest-common').forEach(x =>
                    codesList.push(x.id.replace('quest-', '')));
                let answersResp = await fetch('/answers/', {
                    method: 'GET'
                });
                let allAnswers = await answersResp.json();
                for (let q of codesList) {
                    let answers = allAnswers.filter(item => item.user === userId && item.quest_code === q);
                    if (answers.length > 0) {
                        function compare(a, b) {
                            if (a.id < b.id) {
                                return -1;
                            }
                            if (a.id > b.id) {
                                return 1;
                            }
                            return 0;
                        }
                        answers.sort(compare);
                        let anwswerLast = answers[answers.length - 1];
                        if (!anwswerLast.is_cleared) {
                            let qIdResp = await fetch('/questions/' + anwswerLast.id_quest, {
                                method: 'GET'
                            });
                            let qId = await qIdResp.json();
                            let blockId = qId['test'];
                            let answerList = JSON.parse(anwswerLast.answers);
                            if (anwswerLast.is_textvalue) {
                                let inputAnswer = document.getElementById(`quest-${q}`);
                                inputAnswer.value = answerList[0];
                                inputAnswer.disabled = true;
                                if (inputAnswer.tagName === "TEXTAREA") {
                                    editor.getDoc().setValue(answerList[0]);
                                    editor.setOption("readOnly", true);
                                    console.log(anwswerLast.auto_tests)
                                    let testBlock = document.getElementById('auto-tests')
                                    let htmlStr = '';
                                    let tests = anwswerLast.auto_tests
                                        .substr(0, anwswerLast.auto_tests.length - 1)
                                        .split(';');
                                    for (let line of tests) {
                                        htmlStr += '<div class="auto-tests-block">';
                                        let elems = line.split('*');
                                        htmlStr += elems[0] === "True" ? "<i class=\"fa fa-check correct-res\"\n aria-hidden=\"true\"></i>" :
                                            '<i class="fa fa-times wrong-res" aria-hidden="true"></i>';

                                        htmlStr += `<span class="quest-result auto-test"> ${elems[1]}</span></div>`
                                    }
                                    testBlock.innerHTML = htmlStr;
                                }
                            } else {
                                let allInputs = document.querySelectorAll(`#quest-${q} input`);
                                allInputs.forEach(item => item.disabled = true);
                                for (let answerN of answerList) {
                                    let inputAnswer = document.getElementById(`answer-${q}-${answerN}`);
                                    inputAnswer.checked = true;
                                }
                            }

                            let results = document.querySelectorAll('.quest_result');
                            results.forEach((elem) => {
                                if (elem.id === `res-${q}`) {

                                    if (anwswerLast.is_correct) {
                                        elem.innerHTML = "<i class=\"fa fa-check correct-res\" aria-hidden=\"true\"></i> <span class=\"quest-result\">Верно</span>";
                                    } else {
                                        elem.innerHTML = "<i class=\"fa fa-times wrong-res\" aria-hidden=\"true\"></i> <span class=\"quest-result\">Неверно</span>";
                                    }
                                }
                            });
                            document.getElementById(`button-${blockId}`).style.display = "block";
                        }
                    }

                }
            }
        }
    }

    function change() {
        img[index].className = 'theme-slide';
        index = (index + 1) % img.length;
        img[index].className = 'theme-slide showing';
        window.location.hash = index;
        window.scrollTo(0, 0);
        if (index === 0) {
            goNextTheme();
        }
        addUserSlide();
        renderUserAnswers();

    }

    function initialize() {
        let anc = window.location.hash.replace("#", "");
        if (anc !== "") {
            index = +anc;
            for (let i = 0; i < img.length; i++)
                img[i].className = 'theme-slide';
            img[index].className = 'theme-slide showing';
        } else {
            for (let i = 1; i < img.length; i++)
                img[i].className = 'theme-slide';
        }
        addUserSlide();
        renderUserAnswers();

    }

    function goNextTheme() {
        let loc = document.location.pathname;
        let theme_num = +loc.split('/')[2] + 1;
        window.location.hash = '';
        if (theme_num < 17)
            document.location.pathname = "course/" + theme_num;
    }

    let pointers = document.querySelectorAll('.next-slide');
    let linksTheme = document.querySelectorAll('.name-theme');
    linksTheme.forEach(link => link.addEventListener("click", () => setTimeout(initialize, 500)));
    pointers.forEach(pointer => pointer.addEventListener("click", change));
    initialize();

}

function ValidatePassword(btnId, passId1, passId2, errorId) {
    let passw = document.getElementById(passId1);
    let passw2 = document.getElementById(passId2);
    let re = /(?=.*[0-9])(?=.*[a-z])[0-9a-zA-Z!@#$%^&*]{8,}/g;
    let btn = document.getElementById(btnId);
    passw.oninput = (e) => CheckPassword(passw, passw2, btn, re, errorId);
    passw2.oninput = (e) => CheckPassword(passw, passw2, btn, re, errorId);
}

function getLocalDateTime() {
    const date = new Date();
    const offset = date.getTimezoneOffset();
    const MS_PER_MINUTE = 60000;
    let dateStr = document.getElementsByClassName('review-date-wrap');
    for (let dateItem of dateStr) {
        let d = Date.parse(dateItem.innerText);
        let myStartDate = new Date(d - offset * MS_PER_MINUTE);
        let parts  = myStartDate.toLocaleString().split(', ');
        let timeParts = parts[1].split(':');
        dateItem.innerText = `${parts[0]} в ${timeParts[0]}:${timeParts[1]}`;
    }
}

function CheckPassword(passw, passw2, btn, re, errorId) {
    if (passw.value.search(re) === -1) {
        btn.disabled = true;
        document.getElementById(errorId).innerText = "В пароле должно быть минимум 8 символов," +
            "только латинские буквы, хотя бы одна цифра, могут содержаться спецсимволы: !@#$%^&*";
    } else if (passw.value !== passw2.value) {
        btn.disabled = true;
        document.getElementById(errorId).innerText = "Пароли должны совпадать";
        console.log(document.getElementById(errorId).innerText);
    } else {
        btn.disabled = false;
        document.getElementById(errorId).innerText = "";
    }
}



