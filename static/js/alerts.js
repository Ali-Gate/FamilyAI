function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

document.addEventListener("DOMContentLoaded", async () => {
  try {
    console.log("Fetching notifications...");
    const response = await fetch("/api/notifications/", {
      method: "GET",
      headers: {
        Accept: "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      credentials: "same-origin",
    });
    console.log("Response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Response error text:", errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Data received:", data);

    const container = document.getElementById("notifications-container");
    container.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = "<p>No notifications found.</p>";
      return;
    }

    data.forEach((notification) => {
      const unseenClass = notification.is_seen ? "" : "unseen";
      const tickIcon = notification.is_seen
        ? ""
        : `<i class="fa-solid fa-check notif-tick" data-id="${notification.id}" title="Mark as seen"></i>`;

      // Note: changed id="notif-del" to class="notif-del"
      const item = document.createElement("div");
      item.classList.add("notification");
      item.innerHTML = `
            <div class="notif-div ${unseenClass}">
                <div class="notif-icons">
                    ${tickIcon}
                    <i class="fa-solid fa-trash notif-del" data-id="${notification.id}" title="Delete notification"></i>
                </div>
                <strong>${notification.title}</strong><br>
                <small>From: ${notification.ticket_creator || "System"}</small><br>
                <p>${notification.description}</p>
                <hr>
            </div>
            `;
      container.appendChild(item);
    });

    // Attach event listeners to all tick icons AFTER rendering
    container.querySelectorAll(".notif-tick").forEach((icon) => {
      icon.addEventListener("click", async (e) => {
        const notifTick = e.target;
        const notifDiv = notifTick.closest(".notif-div");
        const notifId = notifTick.getAttribute("data-id");

        try {
          const patchResponse = await fetch(`/api/notifications/${notifId}/`, {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrftoken,
              Accept: "application/json",
            },
            body: JSON.stringify({ is_seen: true }),
            credentials: "same-origin",
          });

          if (!patchResponse.ok) {
            const errorText = await patchResponse.text();
            console.error(`Failed to mark as seen: ${errorText}`);
            return;
          }

          // Remove tick icon
          notifTick.remove();

          // Remove 'unseen' class to revert background
          notifDiv.classList.remove("unseen");
        } catch (error) {
          console.error("Error updating notification:", error);
        }
      });
    });

    // Attach event listeners to all delete icons AFTER rendering
    container.querySelectorAll(".notif-del").forEach((icon) => {
      icon.addEventListener("click", async (e) => {
        const notifDel = e.target;
        const notifDiv = notifDel.closest(".notification");
        const notifId = notifDel.getAttribute("data-id");

        if (!confirm("Are you sure you want to delete this notification?")) {
          return;
        }

        try {
          const deleteResponse = await fetch(`/api/notifications/${notifId}/`, {
            method: "DELETE",
            headers: {
              "X-CSRFToken": csrftoken,
              Accept: "application/json",
            },
            credentials: "same-origin",
          });

          if (!deleteResponse.ok) {
            const errorText = await deleteResponse.text();
            console.error(`Failed to delete notification: ${errorText}`);
            return;
          }

          // Remove the whole notification from DOM
          notifDiv.remove();
        } catch (error) {
          console.error("Error deleting notification:", error);
        }
      });
    });

  } catch (error) {
    console.error("Error fetching notifications:", error);
    const container = document.getElementById("notifications-container");
    if (container) container.innerText = "Failed to load notifications.";
  }
});