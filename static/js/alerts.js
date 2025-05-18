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
  
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Response error text:", errorText);
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const data = await response.json();
      const container = document.getElementById("notifications-container");
      container.innerHTML = "";
  
      if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "<p>No notifications found.</p>";
        return;
      }
  
      // Sort to show unseen notifications first
      data.sort((a, b) => (a.is_seen === b.is_seen ? 0 : a.is_seen ? 1 : -1));
  
      // Highlight the bell if there are any unseen notifications
      const bellIcon = document.querySelector(".notif-bell");
      if (data.some(n => !n.is_seen) && bellIcon) {
        bellIcon.classList.add("unseen");
      }
  
      data.forEach((notification) => {
        const unseenClass = notification.is_seen ? "" : "unseen";
        const tickIcon = notification.is_seen
          ? ""
          : `<i class="fa-solid fa-check notif-tick" data-id="${notification.id}" title="Mark as seen"></i>`;
  
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
  
      // Tick icon: mark as seen
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
  
            notifTick.remove();
            notifDiv.classList.remove("unseen");
  
            // Re-check if any unseen notifications remain
            const checkResponse = await fetch("/api/notifications/", {
              method: "GET",
              headers: {
                "X-Requested-With": "XMLHttpRequest",
                Accept: "application/json",
              },
              credentials: "same-origin",
            });
  
            if (checkResponse.ok) {
              const allNotifications = await checkResponse.json();
              const stillHasUnseen = allNotifications.some(n => !n.is_seen);
              const bellIcon = document.querySelector(".notif-bell");
  
              if (bellIcon && !stillHasUnseen) {
                bellIcon.classList.remove("unseen");
              }
            }
          } catch (error) {
            console.error("Error updating notification:", error);
          }
        });
      });
  
      // Trash icon: delete notification
      container.querySelectorAll(".notif-del").forEach((trashIcon) => {
        trashIcon.addEventListener("click", async (e) => {
          const notifId = e.target.getAttribute("data-id");
          const notifDiv = e.target.closest(".notification");
  
          try {
            const deleteResponse = await fetch(`/api/notifications/${notifId}/`, {
              method: "DELETE",
              headers: {
                "X-CSRFToken": csrftoken,
                Accept: "application/json",
              },
              credentials: "same-origin",
            });
  
            if (deleteResponse.ok) {
              notifDiv.remove();
  
              // After deletion, check again for unseen notifs
              const checkResponse = await fetch("/api/notifications/", {
                method: "GET",
                headers: {
                  "X-Requested-With": "XMLHttpRequest",
                  Accept: "application/json",
                },
                credentials: "same-origin",
              });
  
              if (checkResponse.ok) {
                const allNotifications = await checkResponse.json();
                const stillHasUnseen = allNotifications.some(n => !n.is_seen);
                const bellIcon = document.querySelector(".notif-bell");
  
                if (bellIcon && !stillHasUnseen) {
                  bellIcon.classList.remove("unseen");
                }
              }
            } else {
              console.error("Failed to delete notification");
            }
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