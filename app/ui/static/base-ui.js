function getYouHtml(question) {
  return `<div class="event custom-event-you">
    <div class="content">
      <div class="summary">
        <a>YOU</a>
      </div>
      <div class="extra text custom-extra-text custom-chat-text">
        ${question}
      </div>
      <div class="meta">
      </div>
    </div>
  </div>
  `
}

function getAiHtml(answer, reference_documents, documentIndex) {
  let reference_texts = '<div class = "ui bulleted list" >'
  for (let idx in reference_documents) {
    console.log(reference_documents[idx])
    reference_texts += `
      <div class="item" > ${reference_documents[idx]['content']} </div>
    `
  }
  reference_texts += '</div>'

  return `
  <div class="event custom-event-ai">
    <div class="content">
      <div class="summary">
        <a>AI</a> <span style="color: #000000;"></span>
      </div>
      <div class="extra text custom-extra-text custom-chat-text">
        ${answer}
      </div>
      <div class="meta">
      </div>
    </div>
  </div>
  
  <div class="ui fluid accordion">
    <div class="title">
      <i class="dropdown icon"></i>
      ${documentIndex}
    </div>
    <div class="content">
      ${reference_texts}
    </div>
  </div>
  `
}

function getDocuments(callback) {
  $.ajax({
    url: "/documents",
    type: "GET",
    success: function (result) {
      callback(result)
    },
    error: function (error) {
      console.log(error)
    }
  })
}

function deleteDocuments(documentIndex, success, fail) {
  $.ajax({
    url: `/documents/${documentIndex}`,
    type: "DELETE",
    success: function (result) {
      success(result)
    },
    error: function (error) {
      fail(error)
    }
  })
}

function uploadDocument(file, documentIndex, chunkSize, chunkOverlap, success, fail) {
  const data = new FormData();
  data.append('file', file);
  $.ajax({
    url: `/documents/${documentIndex}?chunk=${chunkSize}&overlap=${chunkOverlap}`,
    type: "POST",
    data: data,
    headers: {
      'Accept': 'application/json',
    },
    crossDomain: true,
    contentType: false,
    processData: false,
    dataType: 'json',
    cache: false,
    success: function (result) {
      success(result)
    },
    error: function (error) {
      fail(error)
    }
  })
}

function getAnswer(question, callback) {

  $.ajax({
    url: `/answer/${question}`,
    type: "GET",
    success: function (result) {
      callback(result)
    },
    error: function (error) {
      console.log(error)
    }
  })
}

function getAnswerWithRetrieval(documentIndex, question, k, callback) {
  $.ajax({
    url: `/answer/${documentIndex}/${question}?k=${k}`,
    type: "GET",
    success: function (result) {
      callback(result)
    },
    error: function (error) {
      console.log(error)
    }
  })
}

function activeProgress() {
  $('#custom-progress-icon').addClass('active')
}

function inactiveProgress() {
  $('#custom-progress-icon').removeClass('active')
}

function initializeAccordion() {
  $('.ui.accordion')
    .accordion()
  ;
}

window.addEventListener('DOMContentLoaded', function () {
  // Set input enter event
  let sendButton = document.getElementById('custom-send-button')
  let questionInput = document.getElementById('custom-question-input')
  questionInput.addEventListener("keypress", function (event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      sendButton.click();
    }
  });

  // Set input send event
  sendButton.addEventListener('click', function () {
    // Get chat ui
    let feeds = document.getElementById('custom-feeds')

    // Update question to View
    let question = document.getElementById('custom-question-input').value
    feeds.insertAdjacentHTML('beforeend', getYouHtml(question))
    feeds.scrollIntoView(false);

    // Remove special character
    let reg = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/]/gim;
    question = question.replace(reg, '')

    // Update answer to View
    activeProgress()
    let dropdownMenu = document.getElementById('custom-indices-dropdown-menu')
    let selects = dropdownMenu.getElementsByClassName("selected");
    let k = 5
    if (selects.length > 0) {
      let documentIndex = selects[0].getAttribute('data-value')
      console.log(`${documentIndex} is selected - Call LLM model with Retrieval`)
      getAnswerWithRetrieval(documentIndex, question, k, function (result) {
        console.log(result)
        let answer = result['result']
        let referenceDocuments = result['reference_documents']
        feeds.insertAdjacentHTML('beforeend', getAiHtml(answer, referenceDocuments, documentIndex))
        feeds.scrollIntoView(false);
        initializeAccordion()
        inactiveProgress()
      })
    } else {
      console.log('Document not selected - Call Only LLM model')
      getAnswer(question, function (result) {
        console.log(result)
        let answer = result['result']
        feeds.insertAdjacentHTML('beforeend', getAiHtml(answer, [], '-'))
        feeds.scrollIntoView(false)
        initializeAccordion()
        inactiveProgress()
      })
    }

    // Clean
    document.getElementById('custom-question-input').value = ""
  })


  // Set dropdown and document list event
  let dropDownMenu = document.getElementById('custom-indices-dropdown-menu')
  let deleteDocumentList = document.getElementById('custom-documents-deletion')

  function loadDocuments(callback) {
    getDocuments(function (result) {
      dropDownMenu.innerHTML = ''
      deleteDocumentList.innerHTML = ''
      for (let idx in result) {
        // Set to Documents for retrieval
        let menuHtml = `<div class="item" data-value="${result[idx]}">${result[idx]}</div>`
        dropDownMenu.insertAdjacentHTML('beforeend', menuHtml)

        // Set to Documents for delete
        let deleteHtml = `
          <a class="item">
            ${result[idx]}
            <div class="ui orange horizontal label custom-del-items" data-value="${result[idx]}">DEL</div>
          </a>
          `
        let conditions = ['doc-ant-grasshoper', 'doc-little-red-hood', 'doc-tortoise-hare']
        if (conditions.some(el => result[idx].includes(el))) {
          deleteHtml = `
          <a class="item">
            ${result[idx]}
            <div class="ui green horizontal label" data-value="${result[idx]}">doc-</div>
          </a>
          `
        }

        deleteDocumentList.insertAdjacentHTML('beforeend', deleteHtml)
      }

      $('#custom-documents-selection')
        .dropdown({
          clearable: true
        })
      if (callback) {
        callback(result)
      }
    })
  }

  activeProgress()
  loadDocuments(function (result) {
    inactiveProgress()
  })

  // Set document delete event
  $(document).on('click', ".custom-del-items", function (event) {
    event.stopPropagation();
    event.stopImmediatePropagation();

    let sendButton = $(event.target);
    let documentIndex = sendButton.attr('data-value')
    console.log(documentIndex)

    activeProgress()
    deleteDocuments(documentIndex, function (result) {
      console.log(result)
      loadDocuments(function (result) {
        inactiveProgress()
      })
    }, function (error) {
      console.log(error)
      inactiveProgress()
    })
  });

  // Set file input event
  $(document).on('change', '#custom-file-input', function (event) {
    if (this.files.item.length > 0) {
      let filename = this.files.item(0).name.replace(/\.[^/.]+$/, "")
      let regex = /[^A-Za-z0-9]/g;
      filename = filename.replace(regex, '-').slice(0, 15)
      $('#custom-doc-name-input').val(filename.toLowerCase())
    }
  })


  function makeRandom(length) {
    let result = '';
    const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
  }

  function cleanForm() {
    document.getElementById("custom-file-input").value = "";
    $('#custom-doc-name-input').val('')
    $('#custom-doc-chunk-input').val(1000)
    $('#custom-doc-overlap-input').val(0)
  }

  // Set file upload event
  $(document).on('click', "#custom-doc-upload", function (event) {
    event.stopPropagation();
    event.stopImmediatePropagation();
    let documentFileInput = document.getElementById("custom-file-input");
    let documentFile = documentFileInput.files[0]
    let documentIndex = $('#custom-doc-name-input').val()
    let chunkSize = $('#custom-doc-chunk-input').val()
    let chunkOverlap = $('#custom-doc-overlap-input').val()

    // Refine documentIndex
    let regex = /[^A-Za-z0-9]/g;
    documentIndex = documentIndex.replace(regex, '-').slice(0, 15).toLowerCase()
    documentIndex = `doc-${documentIndex}-${makeRandom(3)}`

    activeProgress()
    uploadDocument(documentFile, documentIndex, chunkSize, chunkOverlap, function (result) {
      console.log(result)
      loadDocuments(function (result) {
        cleanForm()
        inactiveProgress()
      })
    }, function (error) {
      console.log(error)
      inactiveProgress()
      cleanForm()
    })

  });

})
