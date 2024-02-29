// formset_handling.js
(function($) {
    $(document).ready(function() {
        var formsetPrefix = $('#formset').data('formset-prefix');
        var totalForms = $('#id_' + formsetPrefix + '-TOTAL_FORMS');
        var formsetRow = $('.formset-row:first').clone(true);

        $('div[id^="div_id_' + formsetPrefix + '-"][id$="-DELETE"]').hide();

        $('#add-row').click(function() {
            var newForm = formsetRow.clone(true);
            var formCount = parseInt(totalForms.val());

            newForm.find(':input[name]').each(function() {
                var name = $(this).attr('name');
                var id = $(this).attr('id');
                if (name && id) {
                    var newName = name.replace('-0-', '-' + formCount + '-');
                    var newId = id.replace('-0-', '-' + formCount + '-');
                    $(this).attr({'name': newName, 'id': newId}).val('').removeAttr('checked');
                }
            });

            totalForms.val(formCount + 1);
            $('.formset-row:last').after(newForm);
            bindDeleteEvent();
        });

        function bindDeleteEvent() {
            $('.delete-row').off('click').click(function() {
                $(this).closest('.formset-row').find('input[type="checkbox"][name$="DELETE"]').prop('checked', true).hide();
                $(this).closest('.formset-row').hide();
            });
        }

        bindDeleteEvent();
    });
})(jQuery);
