#pragma once

#include <iostream>
#include <log/catalog/mipi_encoder.hpp>
#include <log/log.hpp>

#define LOGGING_ENABLED

#ifdef LOGGING_ENABLED
#define POCLOG_TRACE(...) CIB_LOG(logging::level::TRACE, __VA_ARGS__)
#define POCLOG_INFO(...) CIB_LOG(logging::level::INFO, __VA_ARGS__)
#define POCLOG_WARN(...) CIB_LOG(logging::level::WARN, __VA_ARGS__)
#define POCLOG_ERROR(...) CIB_LOG(logging::level::ERROR, __VA_ARGS__)
#define POCLOG_FATAL(...)                                                      \
  (CIB_LOG(logging::level::FATAL, __VA_ARGS__), logging::terminate())
#else
#define POCLOG_TRACE(...)
#define POCLOG_INFO(...)
#define POCLOG_WARN(...)
#define POCLOG_ERROR(...)
#define POCLOG_FATAL(...)
#endif

namespace poc::logs {

struct logger {
  template <typename... Args>
  auto log_by_args(std::uint32_t header, Args... args) {
    std::cout << header << std::endl;
    ([&] { std::cout << args << std::endl; }(), ...);
  }

  template <typename... Args>
  auto log_by_buf(std::uint32_t *buf, std::uint32_t size) const {
    // In this case, buffer could be copied to peripheral buffer
    for (std::uint32_t i = 0; i < size; i++) {
      std::cout << buf[i] << std::endl;
    }
  }
};

struct concurrency_policy {
  template <std::invocable F, std::predicate... Pred>
    requires(sizeof...(Pred) < 2)
  static inline auto call_in_critical_section(F &&f, Pred &&...pred)
      -> decltype(std::forward<F>(f)()) {
    while (true) {
      if ((... and pred())) {
        return std::forward<F>(f)();
      }
    }
  }
};

} // namespace poc::logs

template <>
inline auto logging::config<> =
    logging::mipi::under<poc::logging::concurrency_policy>::config{
        poc::logging::logger{}};
