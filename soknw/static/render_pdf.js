const url = 'http://127.0.0.1:5000/library/get/',
    book_id = document.querySelector('#book_id').textContent;

// const url = 'https://soknow.herokuapp.com/library/get/',
//     book_id = document.querySelector('#book_id').textContent;

let pdfDoc = null,
    pageNum = 1,
    pageIsRendering = false,
    pageNumIsPending = null;

const scale = 1.0,
    cavas = document.querySelector('#pdf-canvas'),
    contex = cavas.getContext('2d');

// Render the page
const renderPage = num =>{
    pageIsRendering = true;

    // get the page
    pdfDoc.getPage(num).then(page =>{
        // set scale
        const viewport = page.getViewport({scale});
        cavas.height = viewport.height;
        cavas.width = viewport.width;

        const renderContext = {
            canvasContext : contex,
            viewport
        }
        page.render(renderContext).promise.then(() => {
            pageIsRendering = false;
            if(pageNumIsPending != null ){
                renderPage(pageNumIsPending);
                pageNumIsPending = null;
            }

        });

        //  output current page
        document.querySelector('#page-num').textContent = num;
    });

};

// check for page rendering
const queueRenderPage = num => {
    if (pageIsRendering){
        pageIsRendering = num;
    } else {
        renderPage(num);
    }
} 

// Show Previous Page
const showPrevPage = () => {
    if (pageNum <= 1){
        return;
    }
    pageNum--;
    queueRenderPage(pageNum)
}


// Show Next Page
const showNextPage = () => {
    if (pageNum >= pdfDoc.numPages){
        return;
    }
    pageNum++;
    queueRenderPage(pageNum)
}



// Get Document
pdfjsLib.getDocument(url.concat(book_id)).promise.then(pdfDoc_ => {
    pdfDoc = pdfDoc_;
    document.querySelector('#page-count').textContent = pdfDoc.numPages;
    renderPage(pageNum)
});

// Button Event
document.querySelector('#prev-page').addEventListener('click', showPrevPage);
document.querySelector('#next-page').addEventListener('click', showNextPage);
