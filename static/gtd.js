function addListItem(data) {
  let dateDiff = (Date.now() - Date(data.date)) / (1000 * 3600 * 24);
  $(".list-group").append(
    `<a href="#" class="list-group-item list-group-item-action active" aria-current="true">\
          <div class="d-flex w-100 justify-content-between">\
            <h5 class="mb-1">${data.title}</h5>\
            <small>${dateDiff} days outstanding</small>\
          </div>\
         <p class="mb-1">${data.descr}</p>\
      <small>And some small print.</small>\
    </a>`
  );
}
