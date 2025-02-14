$(document).ready(function () {

    $('.js-example-basic-single').select2();

    function updateFormVisibility(input1_name, input2_name) {
        $('#'+input1_name).css('display', 'none');
        $('#'+input2_name).css('display', 'block');
    }

    // Добавление навыка из текстового поля
    $('#add-button').on('click', function () {
        var selectedSkill = document.getElementById('searchInput').value;
        var skillName = document.getElementById('searchInput').selectedOptions[0].innerText;
    
        if (skillName !== 'Выберите навык') { // Проверка на имя навыка
            var skillList = JSON.parse(getCookie('skillList') || '[]');
            skillList.push({ id: selectedSkill, name: skillName });
            document.cookie = 'skillList=' + JSON.stringify(skillList);
            
            var skill = $('#searchInput option:selected').text();
            skill = skill.slice(1, skill.length-1);
            var skill_id = $('#searchInput option:selected').val();
            if (skill_id !== '') {
                $('#list-container').append('<li data-skill-id="' + skill_id + '">' + skill + ' <button class="remove-button" data-skill-id="' + skill_id + '">Удалить</button></li>');
                var text = $('#skill_list');
                text.val(text.val() + skill + ',');
                $('#searchInput').val(''); // Очистить поле после добавления
                $('#searchInput option[text=""]').prop('selected', true);
            }
        } else {
            // Игнорировать выбор навыка "Выберите навык"
        }
    });
    // // Добавление навыка из текстового поля
    // $('#add-button_1').on('click', function () {
    //     var selectedProfession = document.getElementById('searchInput_1').value;
    //     var ProfessionName = document.getElementById('searchInput_1').selectedOptions[0].innerText;
    
    //     if (ProfessionName !== 'Выберите навык') { // Проверка на имя навыка
    //         var skillList = JSON.parse(getCookie('ProfessionList') || '[]');
    //         skillList.push({ id: selectedProfession, name: ProfessionName });
    //         document.cookie = 'ProfessionList=' + JSON.stringify(skillList);
            
    //         var skill = $('#searchInput_1 option:selected').text();
    //         skill = skill.slice(1, skill.length-1);
    //         var skill_id = $('#searchInput_1 option:selected').val();
    //         if (skill_id !== '') {
    //             $('#list-container').append('<li data-skill-id="' + skill_id + '">' + skill + ' <button class="remove-button" data-skill-id="' + skill_id + '">Удалить</button></li>');
    //             var text = $('#profession_list');
    //             text.val(text.val() + skill + ',');
    //             $('#searchInput_1').val(''); // Очистить поле после добавления
    //             $('#searchInput_1 option[text=""]').prop('selected', true);
    //         }
    //     } else {
    //         // Игнорировать выбор навыка "Выберите навык"
    //     }
    // });
    

    $('#Submit').on('click', function () {
        var skill = $('#searchInput').val();
        if (skill.trim() !== '') {
            $('#list-container').append('<li>' + skill + '</li>');
            $('#searchInput').val(''); // Очистить поле после добавления
        }
    });
});
