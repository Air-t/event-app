$(function(){

  console.log('jolo');

  // confirm delete on click while deleting objects
  $('div.card').on('click', '.delete', function(e){
    var x = confirm("Are you sure you want to delete?");
    return (x) ? true : e.preventDefault()
  })

  // confirm delete on click while deleting objects
  $('div.card').on('click', '.proceed', function(e){
    var x = confirm("Are you sure you want to proceed?");
    return (x) ? true : e.preventDefault()
  })


  function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var addButtons = $('.add-form-row').each(function(e){
      $(this).children().first().attr('src', '/static/webfonts/minus-circle-solid.svg')
    })
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset]):not([name=csrfmiddlewaretoken]):not([type=button])').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;

        $(this).attr({'name': name, 'id': id}).val('');
        if ($(this).attr('type') === 'checkbox') {
          $(this).removeAttr('value');
          $(this).prop("checked", false);
        }

        // if ($(this).attr('type') === 'hidden') {
        //   console.log('here');
        //   $(this).attr({'name': name, 'id': id});
        // } else if ($(this).attr('type') === 'checkbox') {
        //   $(this).removeAttr('value');
        // } else {
        //   $(this).attr('{'name': name, 'id': id}').val('');
        // }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
    .removeClass('btn-secondary').addClass('btn-danger')
    .removeClass('add-form-row').addClass('remove-form-row')
    // conditionRow.find('img').first().attr('src', '/static/webfonts/minus-circle-solid.svg')
    var lastRow = $('.form-row:last').find('img').attr('src', '/static/webfonts/plus-circle-solid.svg')

    return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    cloneMore('.form-row:last', 'form');
    return false;
});
$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});


})
