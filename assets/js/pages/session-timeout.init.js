$.sessionTimeout({
  keepAliveUrl: "../utility/starterpage",
  logoutButton: "Logout",
  logoutUrl: "../authentication/pages-logout",
  redirUrl: "../authentication/pages-lockscreen",
  warnAfter: 3e3,
  redirAfter: 3e4,
  countdownMessage: "Redirecting in {timer} seconds.",
}),
  $("#session-timeout-dialog  [data-dismiss=modal]").attr(
    "data-bs-dismiss",
    "modal"
);