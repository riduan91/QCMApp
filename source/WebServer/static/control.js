
function createGroups(str_nb){
    var nb = parseInt(str_nb);

    if (nb >= 11){
        nb = 10;    
    }
    
    for (var i = 0; i < nb; ++i){
        if (document.getElementById("tablinks_group_" + i) == null){
            $("#group_tab").append("<button type='button' class='tablinks group_" + i + "' id='tablinks_group_" + i + "'>Nhóm câu hỏi " + (i + 1) +"</button>")

            $("#tablinks_group_" + i).click(function(){
                var ix = this.id.slice(15);
                    // Declare all variables
                var j, tabcontent, tablinks;

                // Get all elements with class="tabcontent" and hide them
                tabcontent = document.getElementsByClassName("tabcontent");
                console.log(tabcontent)
                for (j = 0; j < tabcontent.length; j++) {
                    tabcontent[j].style.display = "none";
                }

                // Get all elements with class="tablinks" and remove the class "active"
                tablinks = document.getElementsByClassName("tablinks");
                for (j = 0; j < tablinks.length; j++) {
                   tablinks[j].className = tablinks[j].className.replace(" active", "");
                }

                // Show the current tab, and add an "active" class to the button that opened the tab
                document.getElementById("tabcontent_group_" + ix).style.display = "block";
                this.className += " active";
            })

            $("<table class='tabcontent group_" + i + "' id='tabcontent_group_" + i + "'></table>").insertBefore("#end_tab")
            
            $("#tabcontent_group_" + i)
                .append("<tr><td class='tdbold'>Số người tham gia (để -1 nếu không giới hạn): </td><td><input name='group_nb_players_max_" + i + "' type='number' value=1> người</td><td></td><td></td></tr>")
                .append("<tr><td class='tdbold'>Số câu hỏi: </td><td><input name='group_nb_questions_" + i + "' type='number' value=5></td><td></td><td></td></tr>")                
                .append("<tr><td class='tdbold'>Loại câu hỏi: </td><td><input type='radio' class='group_" + i + "' + name='group_question_type_" + i + "' value=1 checked>Trắc nghiệm</td><td></td><td></td></tr>")
                .append("<tr id='p_nb_options_" + i + "'><td class='tdbold'>Số phương án: </td><td><input name='group_nb_options_" + i + "' type='number' value=4></td><td></td><td></td></tr>")
                .append("<tr><td class='tdbold'>Người chơi được quyền nhìn điểm số của mình: </td><td><input type='radio' name='group_see_self_point_" + i + "' value=1 checked>Có </td><td><input type='radio' name='group_see_self_point_" + i + "' value=0>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Người chơi được quyền nhìn điểm số của người khác: </td><td><input type='radio' name='group_see_other_points_" + i + "' value=1 checked>Có </td><td><input type='radio' name='group_see_other_points_" + i + "' value=0>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Người chơi được quyền nhìn câu trả lời của mình: </td><td><input type='radio' name='group_see_self_answer_" + i + "' value=1 checked>Có </td><td><input type='radio' name='group_see_self_answer_" + i + "' value=0>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Người chơi được quyền nhìn câu trả lời của người khác: </td><td><input type='radio' name='group_see_other_answer_" + i + "' value=1 checked>Có </td><td><input type='radio' name='group_see_other_answer_" + i + "' value=0>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Người chơi được quyền xem đáp án đúng: </td><td><input type='radio' name='group_see_correct_answer_" + i + "' value=1 checked>Có </td><td><input type='radio' name='group_see_correct_answer_" + i + "' value=0>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Người chơi thấy đồng hồ đếm ngược: </td><td><input type='radio' name='group_see_countdown_" + i + "' value=1 checked>Có </td><td><input type='radio' name='group_see_countdown_" + i + "' value=0>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Chuyển qua câu hỏi kế tiếp: </td><td><input type='radio' name='group_next_question_on_" + i + "' value=1>Tự động </td><td><input type='radio' name='group_next_question_on_" + i + "' value=0 checked>Người điều khiển bấm</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Thời gian suy nghĩ / tổng nhóm câu hỏi (để -1 nếu không giới hạn): </td><td><input name='group_group_duration_" + i + "' type='number' value='-1'> giây</td><td></td><td></td></tr>")
                .append("<tr><td class='tdbold'>Thời gian giới hạn cho mỗi câu hỏi (để -1 nếu vô hạn): </td><td><input name='group_question_duration_" + i + "' type='number' value='-1'> giây</td><td></td><td></td></tr>")
                .append("<tr><td class='tdbold'><h3 id='group_method_" + i + "'>Cách chơi: </h3></td><td></td><td></td><td></td></tr>")
                .append("<tr><td class='tdbold'>Điểm chỉ được tính đến: </td><td><input type='radio' name='group_answer_mode_" + i + "' value=0>Người trả lời nhanh nhất </td><td><input type='radio' name='group_answer_mode_" + i + "' value=1 checked>Người trả lời đúng và nhanh nhất</td><td><input type='radio' name='group_answer_mode_" + i + "' value=2>Tất cả</td></tr>")
                .append("<tr><td class='tdbold'>Có quyền chọn Ngôi sao hy vọng: </td><td><input type='radio' class='group_" + i + "' + name='group_stars_accepted_" + i + "' value=1>Có </td><td><input type='radio' name='group_stars_accepted_" + i + "' value=0 checked>Không</td><td></td></tr>")
                .append("<tr><td class='tdbold'>Số Ngôi sao hy vọng mỗi người được có: (để -1 nếu không giới hạn) </td><td><input name='group_nb_stars_" + i + "' type='number' value=-1></td><td></td><td></td></tr>")
                .append("<tr><td class='tdbold'>Trả lời đúng sẽ cộng: </td><td><input name='group_bonus_" + i + "' type='number' value=0> điểm, </td><td>sai bị trừ </td><td><input name='group_penalty_" + i + "' type='number' value=0> điểm</td></tr>")              
                .append("<tr><td class='tdbold'>Trả lời sai sẽ mất lượt trong câu tiếp theo: </td><td><input type='radio' name='group_lose_turn_" + i + "' value=1 >Có </td><td><input type='radio' name='group_lose_turn_" + i + "' value=0 checked>Không</td><td></td></tr>")
                                    
            $("input[name=question_type_" + i + "]").change(function(){
                var ix = this.name.slice(14);
                if (this.value == 1){
                    $("#tabcontent_group_" + ix).append("<tr id='p_nb_options_" + ix + "'><td class='tdbold'>Số phương án: <input name='nb_options_" + ix + "' type='number' value=4></td><td></td><td></td></tr>")              
                }  else {
                    $("#p_nb_options_" + ix).remove();
                }          
            })          

            $("input[name=group_stars_accepted_" + i + "]").change(function(){
                var ix = this.name.slice(21);
                if (this.value == 1){
                    $("#tabcontent_group_" + ix).append("<tr id='group_star_bonus_penalty_" + ix + "'><td class='tdbold'>Có ngôi sao hy vọng, trả lời đúng sẽ cộng: </td><td><input name='group_star_bonus_" + ix + "' type='number' value=0> điểm, sai bị trừ </td><td><input name='group_star_penalty_" + ix + "' type='number' value=0> điểm </td><td></td></tr>")  
                    $("#tabcontent_group_" + ix).append("<tr id='group_star_lose_turn_" + ix + "'><td class='tdbold'>Có ngôi sao hy vọng, trả lời sai bị mất lượt:  </td><td><input type='radio' name='group_star_lose_turn_" + ix + "' value=1 >Có </td><td><input type='radio' name='group_star_lose_turn_" + ix + "' value=0 checked>Không</td><td></td></tr>")  
                                
                }  else {
                    $("#group_star_bonus_penalty_" + ix).remove();
                    $("#group_star_lose_turn_" + ix).remove();
                }          
            })            
        }
    }

    for (var i = nb; i < 11; ++i){
        if (document.getElementById("tablinks_group_" + i) != null)
            $(".group_" + i).remove();
    }

    if (nb > 0){
        document.getElementById("tablinks_group_0").click();    
    }
}

