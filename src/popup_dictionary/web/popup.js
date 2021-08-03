// Custom JS that is added as a script element to Reviewer HTML
console.log("tooltip.js loaded");
// Create the tooltips only when document ready
$(document).ready(function () {
  function focusTooltip(focusedElement) {
    document.querySelectorAll(".qtip").forEach((otherQtipElm) => {
      otherQtipElm.classList.add("tt-disabled");
    });
    focusedElement.classList.remove("tt-disabled");
  }


  function createTooltip(element) {
    // Creates tooltip on specified DOM element, sets up mouse click events
    // and child tooltips, returns tooltip API object

    // create qtip on Anki qa div and assign its api object to 'tooltip'
    var tooltip = $(element)
      .qtip({
        content: {
          text: "Loading...",
        },
        prerender: true, // need to prerender for child tooltips to work properly
        // draw on mouse position, but don't update position on mousemove
        position: {
          target: "mouse",
          viewport: $(document), // constrain to window
          adjust: {
            mouse: false, // don't follow mouse
            method: "flip", // adjust to viewport by flipping tip if necessary
            scroll: false, // buggy, disable
          },
        },
        // apply predefined style
        style: {
          classes: "qtip-bootstrap",
        },
        // don't set up any hide event triggers, do it manually instead
        hide: false,
        // wait until called upon
        show: false,
        events: {
          hide: function (event, api) {
            // hide next nested tooltip on hide
            var ttID = api.get("id");
            var ttIDnext = "#qtip-" + (ttID + 1);
            $(ttIDnext).qtip("hide");
          },
        },
      })
      .qtip("api");

    const qtipElm = tooltip.tooltip[0];
    const footerElm = document.createElement("div");
    footerElm.innerHTML = `Pop-up Dictionary v${_pDictVersion} by <a class='tt-footer-link' href='${_pDictLink}'>Glutanimate</a>`;
    footerElm.classList.add("tt-footer");
    qtipElm.appendChild(footerElm);

    $(qtipElm).mouseenter(function() {
        focusTooltip(qtipElm);
    })

    // Custom double click event handler that works across
    // element boundaries → support for dblclick-holding and
    // then releasing over different DOM element (e.g. boldened text)

    var clicks = 0,
      delay = 500;

    $(element).on("mousedown", function (event) {
      clicks++;

      setTimeout(function () {
        clicks = 0;
      }, delay);

      if (clicks === 2) {
        event.stopImmediatePropagation();
        $(document).one("mouseup", function (event) {
          showTooltip(event, tooltip, element);
          clicks = 0;
          return;
        });
      } else {
        tooltip.hide();
      }
    });

    return tooltip;
  }

  getSelected = function () {
    return (
      (window.getSelection && window.getSelection()) ||
      (document.selection && document.selection.createRange())
    );
  };

  invokeTooltipAtSelectedElm = function () {
    var selection = getSelected();
    var selElm = selection.getRangeAt(0).startContainer.parentNode;
    var ttBoundElm = $(selElm).closest(".qtip-content");
    if (typeof ttBoundElm[0] === "undefined") {
      ttBoundElm = document.getElementById("qa");
      var tooltip = qaTooltip;
    } else {
      var tooltip = ttBoundElm.qtip("api");
    }
    showTooltip(event, tooltip, ttBoundElm);
  };

  // Look up selected text and show result in provided tooltip
  showTooltip = function (event, tooltip, element) {
    /* event: event that triggered function call
           tooltip: qtip api object of tooltip to use for showing results
           element: element that tooltip is bound to */

    // Prevent immediately hiding invoked tooltip
    if (typeof event !== "undefined") {
      event.stopPropagation();
    }

    // Hide existing tooltip at current nesting level,
    //  this propagates to all child tooltips through the qtip
    //  hide event
    tooltip.hide();

    // Get selection
    var selection = getSelected();
    term = selection.toString().trim();

    // Return if selection empty or too short
    if (term.length < 3) {
      return;
    }

    // Exclude NID of clicked-on result entry
    if (element.id != "#qa") {
      var selElm = selection.getRangeAt(0).startContainer.parentNode;
      var resElm = $(selElm).closest(".tt-res")[0];
      if (resElm && "nid" in resElm.dataset) {
        var selNID = resElm.dataset.nid;
        console.log("Ignore current NID: " + selNID);
      } else {
        var selNID = "";
      }
    }

    // Set tooltip contents through pyrun bridge. Need to use a callback
    // due to async execution of JS and Python in Anki 2.1
    pycmd(
      "popupDictionaryLookup:" + JSON.stringify([term, selNID]),
      function (text) {
        return onCallback(text);
      }
    );

    function onCallback(text) {
      // Silent exit if no results returned and ALWAYS_SHOW in Python False
      if (!text) {
        return;
      }

      // Determine current qtip ID and ID of potential child tooltip
      var ttID = tooltip.get("id");
      var domID = "#qtip-" + ttID;
      var newttID = ttID + 1;
      var newdomID = "#qtip-" + newttID;
      console.log("Current tt domID: " + domID);
      console.log("New tt domID: " + newdomID);

      // Set tooltip content and show it
      tooltip.set("content.text", text);
      console.log("Set text");
      focusTooltip(tooltip.tooltip[0]);
      tooltip.show();
      console.log("Showed tooltip");
      // Need to scroll to top if tooltip has been drawn before
      $(domID + "-content").scrollTop(0);

      // Highlight search term
      $(domID).highlight(term);
      $(".tt-dict").removeHighlight(); // don't highlight term in dictionary elm

      // Nested tooltips
      // create child tooltip for content on current tooltip
      if ($(newdomID).length == 0) {
        // Bind new qtip instance to content of current tooltip
        console.log(
          "Create new tooltip on ID: " +
            domID +
            ". Tooltip will have ID: " +
            newdomID
        );
        createTooltip(domID + "-content");
      } else {
        // Reuse existing qtip instance
        console.log("Found existing tooltip with ID: " + newdomID);
      }
    }
  };

  // set up bindings to close qtip, unless mouseup is registered on qtip itself
  $(document).on("mouseup", function (event) {
    if ($(event.target).closest("#qa, .qtip").length > 0) {
      return;
    }
    event.stopImmediatePropagation();
    qaTooltip.hide();
  });

  qaTooltip = createTooltip("#qa");
});
