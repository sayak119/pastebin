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

var reg_dereg = function(id) {
    var username = id.substring(1);
    $(document).delegate(id, 'click', function(e) {
        e.preventDefault();
        $.ajax({
            url: 'http://127.0.0.1:8080/admin/register_deregister',
            type: 'POST',
            data: {
                'username': username,
            },
            success: function(response) {
                console.log(response);
                if(response.type == 1)
                    $(id).html('Register As Admin');
                else
                    $(id).html('Deregister As Admin');
            },
            error: function(response) {
                console.log(response);
            }
        });
    });
};

$(document).ready(function() {
    $.ajax({
        url: "http://127.0.0.1:8080/api/allusers",
        type: 'POST',
        success: function(response) {
            Table = document.getElementById('all_users_table');
            allusers_list = response.users;
            username = response.username;
            for (var i = 0; i < allusers_list.length; i++) {
                var tableRow = Table.insertRow(-1);
                var user_link = document.createElement('td');
                user_link.setAttribute('scope', 'row');
                var link = document.createElement('a');
                link.setAttribute('href', 'http://127.0.0.1:8080/' + allusers_list[i].username + '/paste');
                link.innerHTML = allusers_list[i].username;
                user_link.appendChild(link);
                tableRow.appendChild(user_link);
                tableRow.insertCell(1).innerHTML = allusers_list[i].email;
                var type = "";
                var make_del = document.createElement('button');
                make_del.innerHTML = "";
                var temp = allusers_list[i].username;
                make_del.setAttribute('id', allusers_list[i].username);
                if (allusers_list[i].user_type == 1) {
                    type = "Normal";
                    make_del.innerHTML = "Register as Admin";
                } else {
                    type = "Administrator";
                    make_del.innerHTML = "Deregister as Admin";
                }
                tableRow.insertCell(2).innerHTML = type;
                tableRow.insertCell(3).innerHTML = allusers_list[i].paste_count;
                var make_rem_cell = document.createElement('td');
                make_rem_cell.appendChild(make_del);
                tableRow.appendChild(make_rem_cell);
            }
            for (i = 0; i < allusers_list.length; i++) {
                var id = '#' + allusers_list[i].username;
                reg_dereg(id);
            }
            $('logged_in_user').html(username);
        },
        error: function(response) {
            console.log(response);
        },
    });
});
