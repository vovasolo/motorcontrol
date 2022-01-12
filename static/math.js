$(function() {

    $('#btn_upd').click(function() {
        $.ajax({
            url: '/api/info',
            success: function(data) {
                $('#cur_pos').html(data['cur_pos']);
                $('#tar_pos').html(data['tar_pos']);
                $('#cur_speed').html(data['cur_speed']);
                $('#torque').html(data['torque']);
                $('#m_temp').html(data['m_temp']);
            }
        });
    });

    $('#btn_autoupd').click(function() {
        setInterval(function() {
            $.ajax({
                url: '/api/info',
                success: function(data) {
                    $('#cur_pos').html(data['cur_pos']);
                    $('#tar_pos').html(data['tar_pos']);
                    $('#cur_speed').html(data['cur_speed']);
                    $('#torque').html(data['torque']);
                    $('#m_temp').html(data['m_temp']);
                }
            });
        }, 500);
    });

    $('#btn_start').click(function() {
        //console.log(url);
        var pos = document.getElementById('set_pos').value;
        var speed = document.getElementById('set_speed').value;
        var accel = document.getElementById('set_accel').value;
        var decel = document.getElementById('set_decel').value;
        $.ajax({
            url : '/api/move?pos=' + pos + '&speed=' + speed + '&accel=' + accel + '&decel=' + decel,
            success: function(data) {
                ;
            }
        });
    });

    $('#btn_stop').click(function() {
        $.ajax({
            url : '/api/stop',
            success: function(data) {
                ;
            }
        });
    });    

})
