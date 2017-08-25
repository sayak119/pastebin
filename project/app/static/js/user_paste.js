$(document).ready(function() {
    $(".search").keyup(function() {
        var searchTerm = $(".search").val();
        var listItem = $('.table tbody').children('tr');
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('");

        $.extend($.expr[':'], {
            'containsi': function(elem, i, match, array) {
                return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
            }
        });

        $(".table tbody tr").not(":containsi('" + searchSplit + "')").each(function(e) {
            $(this).attr('visible', 'false');
        });

        $(".table tbody tr:containsi('" + searchSplit + "')").each(function(e) {
            $(this).attr('visible', 'true');
        });

    });
});

var delete_post = function(id) {
    $(document).delegate(id, 'click', function(e) {
        e.preventDefault();
        if (confirm('Are You Sure You Want To Delete This Paste?') === true) {
            $.ajax({
                url: $(id).attr('href'),
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    window.location = "http://127.0.0.1:8080/paste";
                },
                error: function(response) {
                    console.log(response);
                    window.location = "http://127.0.0.1:8080/paste";
                }
            });
        }
    });
};

$(document).ready(function() {
    link = window.location.href;
    user_link = link.substring(0, link.length - 6)
    $.ajax({
        url: user_link + '/api/paste',
        type: 'POST',
        success: function(response) {
            // console.log(response);
            Table = document.getElementById('paste_table');
            paste_list = response.paste_list;
            console.log(paste_list);
            username = response.username;
            for (var i = 0; i < paste_list.length; i++) {
                var tableRow = Table.insertRow(-1);
                var title_link = document.createElement('td');
                title_link.setAttribute('scope', 'row');
                var link = document.createElement('a');
                link.setAttribute('href', 'http://127.0.0.1:8080/' + paste_list[i].url);
                link.innerHTML = paste_list[i].title;
                title_link.appendChild(link);
                tableRow.appendChild(title_link);
                tableRow.insertCell(1).innerHTML = paste_list[i].add_time;
                tableRow.insertCell(2).innerHTML = paste_list[i].expire_time;
                tableRow.insertCell(3).innerHTML = paste_list[i].lang;
                var delLink = document.createElement('a');
                delLink.setAttribute('href', 'http://127.0.0.1:8080/' + paste_list[i].url + '/delete');
                delLink.setAttribute('id', 'link_' + i);
                delLink.innerHTML = "<span class='glyphicon glyphicon-remove'></span>";
                edit_del_cell = document.createElement('td');
                edit_del_cell.appendChild(delLink);
                tableRow.appendChild(edit_del_cell);

            }
            for (i = 0; i < paste_list.length; i++) {
                var id = '#link_' + i;
                delete_post(id);
            }
            $('logged_in_user').html(username);
        },
        error: function(response) {
            console.log(response);
        },
    });
});
