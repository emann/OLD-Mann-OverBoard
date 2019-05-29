var clientId = ''; //choose web app client Id, redirect URI and Javascript origin set to http://localhost
var apiKey = ''; //choose public apiKey, any IP allowed (leave blank the allowed IP boxes in Google Dev Console)
var userEmail = ""; //your calendar Id
var userTimeZone = "New_York"; //example "Rome" "Los_Angeles" ecc...
var maxRows = 20; //events to shown
var calName = "YOUR CALENDAR NAME"; //name of calendar (write what you want, doesn't matter)

var scopes = 'https://www.googleapis.com/auth/calendar';

//--------------------- Add a 0 to numbers
function padNum(num) {
  if (num <= 9) {
    return "0" + num;
  }
  return num;
}
//--------------------- end

//--------------------- From 24h to Am/Pm
function AmPm(num) {
  if (num <= 12) {
    return "am " + num;
  }
  return "pm " + padNum(num - 12);
}
//--------------------- end

//--------------------- num Month to String
function monthString(num) {
  if (num === "01") {
    return "JAN";
  } else if (num === "02") {
    return "FEB";
  } else if (num === "03") {
    return "MAR";
  } else if (num === "04") {
    return "APR";
  } else if (num === "05") {
    return "MAJ";
  } else if (num === "06") {
    return "JUN";
  } else if (num === "07") {
    return "JUL";
  } else if (num === "08") {
    return "AUG";
  } else if (num === "09") {
    return "SEP";
  } else if (num === "10") {
    return "OCT";
  } else if (num === "11") {
    return "NOV";
  } else if (num === "12") {
    return "DEC";
  }
}
//--------------------- end

//--------------------- from num to day of week
function dayString(num) {
  if (num == "1") {
    return "mon"
  } else if (num == "2") {
    return "tue"
  } else if (num == "3") {
    return "wed"
  } else if (num == "4") {
    return "thu"
  } else if (num == "5") {
    return "fri"
  } else if (num == "6") {
    return "sat"
  } else if (num == "0") {
    return "sun"
  }
}
//--------------------- end

//--------------------- client CALL
function handleClientLoad() {
  gapi.client.setApiKey(apiKey);
  checkAuth();
}
//--------------------- end

//--------------------- check Auth
function checkAuth() {
  gapi.auth.authorize({
    client_id: clientId,
    scope: scopes,
    immediate: true
  }, handleAuthResult);
}
//--------------------- end

//--------------------- handle result and make CALL
function handleAuthResult(authResult) {
  if (authResult) {
    loadCalendar();
  }
}
//--------------------- end

//--------------------- API CALL itself
function makeApiCall(begin, end, day) {
  gapi.client.load('calendar', 'v3', function() {
    var request = gapi.client.calendar.events.list({
      'calendarId': userEmail,
      'timeZone': userTimeZone,
      'singleEvents': true,
      'timeMin': begin.toISOString(), //gathers only events not happened yet
      'timeMax': end.toISOString(),
      'orderBy': 'startTime'
    });
    request.execute(function(resp) {
      for (var i = 0; i < resp.items.length; i++) {
        var item = resp.items[i];
        var classes = [];
        var allDay = item.start.date ? true : false;
        var startDT = allDay ? item.start.date : item.start.dateTime;
        var dateTime = startDT.split("T"); //split date from time
        var date = dateTime[0].split("-"); //split yyyy mm dd
        var startYear = date[0];
        var startMonth = monthString(date[1]);
        var startDay = date[2];
        var startDateISO = new Date(startMonth + " " + startDay + ", " + startYear + " 00:00:00");
        var startDayWeek = dayString(startDateISO.getDay());
        if (allDay == true) { //change this to match your needs
          var str = [
            startDayWeek, ' ',
            startMonth, ' ',
            startDay, ' ',
            startYear,
            item.summary
          ];
        } else {
          var time = dateTime[1].split(":"); //split hh ss etc...
          var startHour = AmPm(time[0]);
          var startMin = time[1];
          var str = item.summary;
        }
        var list = document.getElementById('cal_day'+day+'_list');
        var entry = document.createElement('li');
        entry.appendChild(document.createTextNode(str));
        list.appendChild(entry);
      }
    });
  });
}
function loadCalendar() {
  var now = new Date(); //today's date
  var today = new Date(now.getTime() - ((now.getTime()-18000000)%86400000));
  for (var i = 1; i < 6; i++) {
    var start = new Date(today.getTime() + 86400000*(i-1));
    var end = new Date(today.getTime() + 86400000*i);
    console.log(start.getTime());
    console.log(end.getTime());
    makeApiCall(start, end, i-1);
  }
}
