/**
 * Created by Filushin_DV on 26.02.15.
 */
    $(function() {
      $( ".datepicker" ).datepicker({
          dateFormat: "yy-mm-dd",
          firstDay: 1,
          monthNames: [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ],
          dayNamesMin: [ "Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб" ]
      });

      $( ".datepicker" ).datepicker();
    });