window.onload = function(){
    var acc = document.getElementsByClassName("accordion");
    var idx;

    for (idx = 0; idx < acc.length; idx++) {
        acc[idx].onclick = function(){
            /* Toggle between adding and removing the "active" class, to highlight the button that controls the panel */
            this.classList.toggle("active");

            /* Toggle between hiding and showing the active panel */
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        }
    }
 
}


function createQuestions(str_i, str_nb, str_options){
    var i = parseInt(str_i);
    var nb = parseInt(str_nb);
    var nb_options = parseInt(str_options);

    if (nb >= 51){
        nb = 50;    
    }

    for (var j = 0; j < nb; ++j){
        if (document.getElementById("tablinks_group_" + i + "_question_" + j ) == null){
            $("#group_tab_" + i).append("<button type='button' class='tablinks_" + i + " group_" + i + "_question_" + j + "' id='tablinks_group_" + i + "_question_" + j + "'>" + (j + 1) +"</button>")

            $("#tablinks_group_" + i + "_question_" + j).click(function(){
                var ix = this.id.substring(15, 16);
                var jx = this.id.slice(26);
                // Declare all variables
                var k, tabcontent, tablinks;

                // Get all elements with class="tabcontent" and hide them
                tabcontent = document.getElementsByClassName("tabcontent_" + i);
                console.log(tabcontent)
                for (k = 0; k < tabcontent.length; k++) {
                    tabcontent[k].style.display = "none";
                }

                // Get all elements with class="tablinks" and remove the class "active"
                tablinks = document.getElementsByClassName("tablinks_" + i);
                for (k = 0; k < tablinks.length; k++) {
                    tablinks[k].className = tablinks[k].className.replace(" active", "");
                }

                // Show the current tab, and add an "active" class to the button that opened the tab
                document.getElementById("tabcontent_group_" + ix + "_question_" + jx).style.display = "block";
                this.className += " active";
            })
    
            $("<table class='tabcontent_" + i + " group_" + i + "_question_" + j + "' id='tabcontent_group_" + i + "_question_" + j  + "'></table>").insertBefore("#end_tab_" + i)

            $("#tabcontent_group_" + i + "_question_" + j)
                .append("<tr><td class='tdbold'>Câu hỏi " + (j + 1) + ": </td><td></td><td class='tdlong'><input name='question_content_" + i + "_" + j + "' type='text'></td></tr>")
            
            var k;
            for (k = 0; k < nb_options; ++k){
                $("#tabcontent_group_" + i + "_question_" + j)
                    .append("<tr><td class='tdbold'>Phương án " + (k+1) + ": </td><td><input type='radio' name='question_answer_" + i + "_" + j + "' value=" + k + " " + (k == 0 ? "checked" : "") + "></td><td class='tdlong'><input name='question_option_" + k + "_" + i + "_" + j + "' type='text'></td></tr>")
            }
        }        
    }

    for (var j = nb; j < 100; ++j){
        if (document.getElementById("tablinks_group_" + i + "_question_" + j) != null)
            $(".group_" + i + "_question_" + j).remove();
    }

    if (nb > 0){
        document.getElementById("tablinks_group_" + i + "_question_0").click();    
    }

    console.log(i);
}

function tabs(i, j){
    // Declare all variables
    var k, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent_" + i);
    console.log(tabcontent)
    for (k = 0; k < tabcontent.length; k++) {
        tabcontent[k].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks_" + i);
    for (k = 0; k < tablinks.length; k++) {
        tablinks[k].className = tablinks[k].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById("tabcontent_group_" + i + "_question_" + j).style.display = "block";
    this.className += " active";
}