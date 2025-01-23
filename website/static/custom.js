// Profile
var proAdmin = document.getElementById('proAdmin');

function openPro() {
    proAdmin.classList.toggle('activePro');
}

document.body.addEventListener('click', function(event) {
    if (!event.target.closest('#proAdmin') && !event.target.closest('#proAdminBtn')) {
        proAdmin.classList.remove('activePro');
    }
});



// Nav and Toggle

var togr = document.getElementById("ul");

function openToggle() {
    togr.classList.toggle('active');
}



// dark and light mode
const body = document.querySelector('body');

function themeMode() {
    body.classList.toggle('theme')
};






//  Filtering the Lists 
// prevent form subissiom
const form = document.querySelector('.hero-input-selects')

form.addEventListener('submit', (e)=>{
    e.preventDefault()
});




// reveal list items on button click
const searchBtns = document.querySelectorAll('.select')
const servicesLists = document.querySelectorAll('.service-option')
const serviceSelect = document.querySelector('.service-select')
const optionLists = document.querySelectorAll('#options .opt-list')
const selectBtnCity = document.querySelector('.city-select')
const CityOptions = document.querySelectorAll('.city-option')
const selectBtnFind = document.querySelector('.wylf-select')
const FindOptions = document.querySelectorAll('.wylf-option')


// mame lists element appear on click of the button
searchBtns.forEach(btn=>{
    const div = document.createElement('div')
    div.classList.add('hidebtn')
    btn.addEventListener('click', ()=>{
        nxtEl = btn.nextElementSibling
        nxtEl.style.display='block';
        x = btn.parentElement
        div.style.display='block'
        x.appendChild(div)
        
               
        optionLists.forEach(list=>{
            list.classList.remove('hide')
        })

        searchInputs.forEach(input=>{
            input.value = '';
        })
    })
    document.addEventListener('click', (e)=>{
        if (!btn.contains(e.target)) {
            div.style.display='none'
        }else{
            div.style.display='block'
        }
    })
    div.addEventListener('click', ()=>{
        div.style.display='none'
    })
})




// change the text on the trong tag element to the li text clicked
serviceList()

function serviceList() {
    servicesLists.forEach(lists =>{
        lists.addEventListener('click', ()=>{
            serviceSelect.innerHTML = lists.innerHTML
        });
    })
}


CityList()

function CityList() {
    CityOptions.forEach(lists =>{
        lists.addEventListener('click', ()=>{
            selectBtnCity.innerText = lists.innerText
        });
    })
}

FindOptions.forEach(lists =>{
    lists.addEventListener('click', ()=>{
        selectBtnFind.innerHTML = lists.innerHTML
    });
})


// all input fields and list item filter
const searchInputs = document.querySelectorAll('.searchinput')

searchInputs.forEach(input=>{
    input.addEventListener('input', (e)=>{
        filterLists(e.target.value)
    })
})

filterLists=(lists)=>{
    optionLists.forEach(list=>{
        if (list.innerText.toLowerCase().includes(lists.toLowerCase())) {
            list.classList.remove('hide')
        }else{
            list.classList.add('hide')
        }
    })
}



// remove any appeared element on click of the document
document.addEventListener('click', (e)=>{
    searchBtns.forEach(btn=>{
        if (!btn.contains(e.target)) {
            nxtEl = btn.nextElementSibling
            nxtEl.style.display='none';
        }
    })
    searchInputs.forEach(input=>{
        if (input.contains(e.target)) {
            x=input.parentElement.parentElement;
            x.style.display='block'
            y = input.parentElement.parentElement.parentElement.lastElementChild
            y.style.display='block'
        }
    })
})



