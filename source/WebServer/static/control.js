
function createGroups(str_nb){
    var nb = parseInt(str_nb);

    if (nb >= 11){
        nb = 10;    
    }
    
    for (var i = 0; i < nb; ++i){
        if (document.getElementById("group_header_" + i) == null){
            $("#common_information").append("<h2 id='group_header_" + i + "' class='group_" + i + "'>Điền các thông tin cho nhóm câu hỏi thứ " + (i + 1) + ":</h2>")
                .append("<p class='group_" + i + "'>Số người tham gia (để -1 nếu không giới hạn): <input name='group_nb_players_max_" + i + "' type='number' value=1> người (có kết quả tốt nhất)</p>")              
                .append("<p class='group_" + i + "'>Người chơi được quyền nhìn điểm số của mình: <input type='radio' name='group_see_self_point_" + i + "' value=1 checked>Có <input type='radio' name='group_see_self_point_" + i + "' value=0>Không</p>")
                .append("<p class='group_" + i + "'>Người chơi được quyền nhìn điểm số của người khác: <input type='radio' name='group_see_other_points_" + i + "' value=1 checked>Có <input type='radio' name='group_see_other_points_" + i + "' value=0>Không</p>")
                .append("<p class='group_" + i + "'>Người chơi được quyền nhìn câu trả lời của mình: <input type='radio' name='group_see_self_answer_" + i + "' value=1 checked>Có <input type='radio' name='group_see_self_answer_" + i + "' value=0>Không</p>")
                .append("<p class='group_" + i + "'>Người chơi được quyền nhìn câu trả lời của người khác: <input type='radio' name='group_see_other_answer_" + i + "' value=1 checked>Có <input type='radio' name='group_see_other_answer_" + i + "' value=0>Không</p>")
                .append("<p class='group_" + i + "'>Người chơi được quyền xem đáp án đúng: <input type='radio' name='group_see_correct_answer_" + i + "' value=1 checked>Có <input type='radio' name='group_see_correct_answer_" + i + "' value=0>Không</p>")
                .append("<p class='group_" + i + "'>Người chơi thấy đồng hồ đếm ngược: <input type='radio' name='group_see_countdown_" + i + "' value=1 checked>Có <input type='radio' name='group_see_countdown_" + i + "' value=0>Không</p>")
                .append("<p class='group_" + i + "'>Chuyển qua câu hỏi kế tiếp: <input type='radio' name='group_next_question_on_" + i + "' value=1>Tự động <input type='radio' name='group_next_question_on_" + i + "' value=0 checked>Người điều khiển bấm</p>")
                .append("<p class='group_" + i + "'>Thời gian suy nghĩ / tổng nhóm câu hỏi (để -1 nếu không giới hạn): <input name='group_group_duration_" + i + "' type='number' value='-1'> giây</p>")
                .append("<p class='group_" + i + "'>Thời gian giới hạn cho mỗi câu hỏi (để -1 nếu vô hạn): <input name='group_question_duration_" + i + "' type='number' value='-1'> giây</p>")
                .append("<h3 id='group_method_" + i + "' class='group_" + i + "'>Cách chơi: </h3>")
                .append("<p class='group_" + i + "'>Điểm chỉ được tính đến: <input type='radio' name='group_answer_mode_" + i + "' value=0>Người trả lời nhanh nhất <input type='radio' name='group_answer_mode_" + i + "' value=1 checked>Người trả lời đúng và nhanh nhất<input type='radio' name='group_answer_mode" + i + "' value=2>Tất cả</p>")
                .append("<p class='group_" + i + "'>Có quyền chọn Ngôi sao hy vọng: <input type='radio' class='group_" + i + "' + name='group_stars_accepted_" + i + "' value=1>Có <input type='radio' name='group_stars_accepted_" + i + "' value=0 checked>Không</p>")
                .append("<p class='group_" + i + "'>Số Ngôi sao hy vọng mỗi người được có: (để -1 nếu không giới hạn) <input name='group_nb_stars_" + i + "' type='number' value=-1></p>")
                .append("<p class='group_" + i + "'>Trả lời đúng sẽ cộng: <input name='group_bonus_" + i + "' type='number' value=0> điểm, sai bị trừ <input name='group_penalty_" + i + "' type='number' value=0> điểm </p>")              
         
            $("input[name=group_stars_accepted_" + i + "]").change(function(){
                console.log(this.name);
                var ix = this.name.slice(21);
                if (this.value == 1){
                    $("#common_information").append("<p id='group_star_bonus_penalty_" + ix + "' class='group_" + ix + "'>Có ngôi sao hy vọng, trả lời đúng sẽ cộng: <input name='group_star_bonus_" + ix + "' type='number' value=0> điểm, sai bị trừ <input name='group_star_penalty_" + ix + "' type='number' value=0> điểm </p>")              
                }  else {
                    $("#group_star_bonus_penalty_" + ix).remove();
                }          
            })            
        }
    }

    for (var i = nb; i < 11; ++i){
        if (document.getElementById("group_header_" + i) != null)
            $(".group_" + i).remove();
    }
    
    if (document.getElementById("submit") == null)
        $("#common_information").append("<input id='submit' type='submit' value='Send'></input>")
}

function changeGroups(str_nb){
    var nb = parseInt(str_nb);

    if (nb >= 11){
        nb = 10;    
    }

    for (var i = nb; i < 11; ++i){
        if (document.getElementById("group_header_" + i) != null)
            $(".group_" + i).remove();
    }

    if (document.getElementById("submit") == null)
        $("#common_information").append("<input id='submit' type='submit' value='Send'></input>")
}