#include "application.hpp"
#include "logging.hpp"

// Logging config specialisation
// template <> inline auto logging::config<> =
// logging::mipi::under<concurrency_policy>::config{logging::console::logger{}};

void application::log_messages() {
  // Basic logging
  POCLOG_TRACE("This is a trace example");
  POCLOG_INFO("This is an info example");
  POCLOG_WARN("This is a warn example");
  POCLOG_ERROR("This is an error example");

  // Formatting
  POCLOG_INFO("This is a format example: {}", 55);
  POCLOG_INFO("This is a second format example: {} {}", 55, 100);

  // Fatal logging
  //POCLOG_FATAL("This is a fatal example");
}