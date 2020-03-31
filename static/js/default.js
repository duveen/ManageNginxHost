function modifyDataTablesLocation(document) {
    let dataTableHeader = document.find('.datatable-header');
    if (dataTableHeader.length === 1) {

        let dataTableLength = document.find('.dataTables_length');
        let dataTableFilter = document.find('.dataTables_filter');

        let header = $("<div class='d-flex'>" +
            "   <div class='text-muted'></div>" +
            "   <div class='ml-auto text-muted'></div> " +
            "</div>");

        header.children().eq(0).append(dataTableLength);
        header.children().eq(1).append(dataTableFilter);

        dataTableHeader.append(header);
    }

    let dataTableFooter = document.find('.datatable-footer');
    if (dataTableFooter.length === 1) {
        let dataTablePages = document.find('.dataTables_paginate');
        dataTablePages.removeClass('dataTables_paginate').removeClass('paging_simple_numbers');
        dataTablePages.addClass('pagination').addClass('m-0').addClass('ml-auto');
        dataTableFooter.append(dataTablePages);
    }
}