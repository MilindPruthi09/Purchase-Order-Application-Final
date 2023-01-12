var numOfCols = 1;
$(document).ready(function () {

  function calculateTotal(currentGroup) {
    var groupTotal = 0;
    currentGroup.parents('table').find('.rowTotal').each(function (i) {
      groupTotal = Number(groupTotal) + Number($(this).text());
    });
    currentGroup.parents('table').find('.total').text(groupTotal.toFixed(2));
    currentGroup.parents('table').find('.subtotal').text(groupTotal.toFixed(2));
  }

  $(".document.active").delegate(".tdDelete", "click", function () {

    if ($(this).parents('tbody').children().length > 1) {
      $(this).prev().text('0');
      calculateTotal($(this));
      var child = $(this).closest('tr').nextAll();
      child.each(function () {
        var id = $(this).attr('id');
        var idx = $(this).children('.row-index').children('p');
        var dig = parseInt(id.substring(1));
        idx.html(`R${dig - 1}`);
        $(this).attr('id', `R${dig - 1}`);
      });

      $(this).parents('tr').remove();

      rowIdx--;
    }
  });

  var rowIdx = 1;
  $(".document.active").delegate(".trAdd", "click", function () {
    numOfCols = numOfCols + 1;
    $('#itemProperties').append(`<tr id="R${++rowIdx}">
    <td class="qty" id="QTY${rowIdx}" contenteditable="true">
    1
    </td>
    <td id="UNT${rowIdx}" contenteditable="true" class="text-center"></td>
    <td id="DESC${rowIdx}" contenteditable="true"></td>
    <td id="DD${rowIdx}" contenteditable="true"></td>
    <td class="amount" id="UP${rowIdx}" contenteditable="true">0</td>
    <td id="TOT${rowIdx}" class="amount amountColumn rowTotal" contenteditable="true">0</td>
    
    <td class="docEdit tdDelete row-index text-center">X</td>
    </tr>`);
  });

  $(".document.active").delegate(".amount", "keyup", function () {
    calculateTotal($(this));
  });

  var tdValues = [];
  $(".document.active .proposedWork").delegate("td:not(.description .unit)", "keyup", function () {
    tdValues.length = 0;
    $(this).parents('tr').find('td').each(function (i) {
      if (i > 5) {
        return false
      }
      if (i == 5) {
        $(this).text(tdValues[0] * tdValues[4])
      }
      tdValues[i] = Number($(this).text());
    });

    calculateTotal($(this));
  });

  if (poNum == "NA") {
    document.getElementById("PONumber").innerHTML = "";

  } else {
    document.getElementById("fromLocation").innerHTML = From;
    document.getElementById("destination").innerHTML = destination;
    document.getElementById("currency").innerHTML = currency;
    document.getElementById("companyDetails").innerHTML = companyNameAndAddress;
    document.getElementById("PONumber").innerHTML = poNum;
    document.getElementById("PODate").innerHTML = PODate;
    document.getElementById("buyer-name").innerHTML = buyerName;
    document.getElementById("vendorDetails").innerHTML = VendorNameAndAddress;
    document.getElementById("importantInstructions").innerHTML = importantInstructions;
    document.getElementById("paymentDetails1").innerHTML = paymentDetailing;
  }
});

function saveIntoDB() {

  // checking for null values
  if (document.getElementById("fromLocation").innerHTML == "") {
    alert("enter from location");
    return false;
  }

  if (document.getElementById("destination").innerHTML == "") {
    alert("enter destination");
    return false;
  }

  if (document.getElementById("currency").innerHTML == "") {
    alert("enter currency");
    return false;
  }

  if (document.getElementById("companyDetails").innerHTML == "") {
    alert("enter company name and address");
    return false;
  }

  if (document.getElementById("PONumber").innerHTML == "") {
    alert("enter PO Number");
    return false;
  }

  if (document.getElementById("PODate").innerHTML == "") {
    alert("enter PO Date");
    return false;
  }

  if (document.getElementById("buyer-name").innerHTML == "") {
    alert("enter Buyer Name");
    return false;
  }

  if (document.getElementById("vendorDetails").innerHTML == "") {
    alert("enter Vendor Details");
    return false;
  }

  if (document.getElementById("importantInstructions").innerHTML == "") {
    alert("enter Important Instructions");
    return false;
  }

  if (document.getElementById("paymentDetails").innerHTML == "") {
    alert("enter Payment Details");
    return false;
  }
  
  var curr=document.getElementById("currency").value;
  // var currValue=curr.value;

  const itemDetails = [];

  var specialSep = " !$ ";

  for (i = 1; i <= numOfCols; i++) {
    itemDetails[i - 1] = {
      po_num: document.getElementById("PONumber").innerHTML,
      qty: document.getElementById(`QTY${i}`).innerText,
      unit: document.getElementById(`UNT${i}`).innerText,
      description: document.getElementById(`DESC${i}`).innerText,
      deliveryDate: document.getElementById(`DD${i}`).innerText,
      UnitPrice: document.getElementById(`UP${i}`).innerText,
      total: document.getElementById(`TOT${i}`).innerText
    };
  }

  $.ajax({
    type: 'POST',
    url: "http://127.0.0.1:5000/itemDetailsUpdate",
    data: JSON.stringify(itemDetails),
    dataType: 'json',
    contentType: 'application/json; charset=utf-8'
  }).done(function (msg) {
    alert("Data Saved: " + msg);
  });

  const myTableArray = [];
  $("table#shipToFrom").each(function () {
    var arrayOfThisRow = [];
    var tableData = $(this).find('td');
    if (tableData.length > 0) {
      tableData.each(function () {
        arrayOfThisRow.push($(this).text());
      });
      myTableArray.push(arrayOfThisRow);
    }
  });

  var from = myTableArray[0][0];
  var destination = myTableArray[0][1];
  var currency = document.getElementById("currency").value;

  const companyNameAddress = [];
  $("table#PO-Details").each(function () {
    var arrayOfThisRow = [];
    var tableData = $(this).find('td');
    if (tableData.length > 0) {
      tableData.each(function () {
        arrayOfThisRow.push($(this).text());
      });
      companyNameAddress.push(arrayOfThisRow);
    }
  });

  var companyDetails = companyNameAddress[0][0];
  var PONumber = companyNameAddress[0][1];
  var PODate = companyNameAddress[0][2];

  const BuyerNameAddress = [];
  $("table#BuyerandVendor").each(function () {
    var arrayOfThisRow = [];
    var tableData = $(this).find('td');
    if (tableData.length > 0) {
      tableData.each(function () {
        arrayOfThisRow.push($(this).text());
      });
      BuyerNameAddress.push(arrayOfThisRow);
    }
  });

  var buyerName = BuyerNameAddress[0][0];
  var vendorDetails = BuyerNameAddress[0][1];
  var impInstructions = BuyerNameAddress[0][2];

  const paymentDetail = [];
  $("table#paymentDetails").each(function () {
    var arrayOfThisRow = [];
    var tableData = $(this).find('td');
    if (tableData.length > 0) {
      tableData.each(function () {
        arrayOfThisRow.push($(this).text());
      });
      paymentDetail.push(arrayOfThisRow);
    }
  });

  var paymentDetailing = document.getElementById("paymentDetails").innerHTML
  
  $.ajax({
    url: "http://127.0.0.1:5000/insertOrder?from=" + from + "&destination=" + destination + "&currency=" +
      currency + "&companyDetails=" + companyDetails + "&PONumber=" + PONumber + "&PODate=" + PODate +
      "&buyerName=" + buyerName + "&vendorDetails=" + vendorDetails + "&impInstructions=" + impInstructions +
      "&paymentDetails=" + paymentDetailing,
    context: document.body
  });
}

function printReport() {
  
  const element = document.getElementById("entirePage");

  html2pdf()
    .from(element)
    .save();
}