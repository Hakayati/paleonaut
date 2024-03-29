// Adapted from anwers.atlassian.com
// Should probably be GPLv3 since OSQA is

(function(){

/**
 * Tag Wizard
 *
 * Expects 'edit_user' variable to be the relative url to POST new settings to,
 * or undefined/false if user is anonymous
 *
 * Requires jQuery UI
 *
 * Use tag_wizard() to open
 */

var products = [
    {name: 'Paleo', id: 'paleo'},
    {name: 'Fett', id: 'fett'},
    {name: 'abnehmen', id: 'abnehmen'},
    {name: 'Fleisch', id: 'fleisch'},
    {name: 'Milchprodukte', id: 'milchprodukte'},
    {name: 'essen', id: 'essen'},
    {name: 'vegetarisch', id: 'vegetarisch'},
    {name: 'Fitness', id: 'fitness'},
    {name: 'Protein', id: 'protein'},
    {name: 'Gesundheit', id: 'gesundheit'},
    {name: 'low-carb', id: 'low-carb'},
]
var development_products = [
    //'Nuxeo DM', 'Nuxeo DAM', 'Nuxeo CMF', 'Nuxeo Marketplace', 'Nuxeo Studio'
]
function tagify(phrase){
    return phrase.toLowerCase().replace(/ /g, '-')
}

var wizard

window.tag_wizard = function(){
    if (!wizard){
        // in case tag_wizard() is called before wizard exists
        setTimeout(tag_wizard, 100)
        return
    }
    wizard.dialog('open')
}

$(function(){
    wizard = $($('#tag-wizard-template').html()).appendTo('body').hide()

    var product = wizard.find('#product'),
        devq = wizard.find('#devq')
    product.append('<option value="">-------</option>')
    $.each(products, function(){
        p = this;
        product.append('<option value="'+p.id+'">'+p.name+'</option>')
    })
    product.change(function(){
        for (var i=0; i<development_products.length; i++)
            if (tagify(development_products[i]) == this.value){
                devq.fadeIn(250)
                return
            }
        devq.fadeOut(250)
    })
    devq.hide()

    // edit_user == undefined if user is anonymous
    if (window.edit_user){
        var noshow = wizard.find('#noshow')
        noshow.change(function(){
            if (noshow.is(':checked')){
                $.ajax({
                    url: edit_user,
                    type: 'POST',
                    data: {show_tag_wizard: false}
                })
                wizard.dialog('close')
            }
            else{
                $.ajax({
                    url: edit_user,
                    type: 'POST',
                    data: {show_tag_wizard: true}
                })
            }
        })

        $.getJSON(edit_user, {show_tag_wizard: ''}, function(data){
            if (data.show_tag_wizard)
                noshow.removeAttr('checked')
            else
                noshow.attr({checked: 'checked'})
        })
    }

    $('<a href="#">Show Tag Wizard</a>')
        .click(function(){
            tag_wizard()
            return false
        })
        .appendTo($('#id_tags').parent())
        .css({float: 'right'})

    wizard.dialog({
        title: 'Tag Auswahl',
        autoOpen: false,
        draggable: true,
        hide: 'fade',
        show: 'fade',
        modal: true,
        width: '30em',
        buttons: {
            OK: function(){
                var tag = product.val()
                if (tag) {
                    var dev = wizard.find('[name=development]:checked').val() == 'true'
                    if (dev)
                        $.each(development_products, function(){
                            if (tagify(String(this)) == tag){
                                tag += '-development'
                                return false
                            }
                        })
                    var tags = $('#id_tags')
                    if (tags.length)
                        if (tags.val())
                            tags.val(tags.val()+' '+tag)
                        else
                            tags.val(tag)
                }
                wizard.dialog('close')
            },
            Cancel: function(){
                wizard.dialog('close')
            }
        }
    })
})

})();
