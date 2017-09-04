window.onload = function(){
    var nb = parseInt(document.getElementById("nb_groups").value);
    document.getElementById("tablinks_group_0").click();    
    for (var i = 0; i < nb; ++i){
                
        
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

function changeGroups(str_nb){
    var nb = parseInt(str_nb);

    if (nb >= 11){
        nb = 10;    
    }


    for (var i = nb; i < 11; ++i){
        if (document.getElementById("tablinks_group_" + i) != null)
            $(".group_" + i).remove();
    }

    if (document.getElementById("submit") == null)
        $("#common_information").append("<input id='submit' type='submit' value='Send'></input>")
}

function openTab(evt, i) {
    // Declare all variables
    var j, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (j = 0; j < tabcontent.length; j++) {
        tabcontent[j].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (j = 0; j < tablinks.length; j++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById("tabcontent_group_" + i).style.display = "block";
    evt.currentTarget.className += " active";
}
