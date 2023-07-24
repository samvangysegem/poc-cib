#pragma once

#include <iostream>
#include <log/log.hpp>
#include <log/level.hpp>
#include <log/catalog/catalog.hpp>

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

namespace {
template <logging::level L, typename S, typename T>
constexpr auto to_message() {
  constexpr auto s = S::value;
  using char_t = typename std::remove_cv_t<decltype(s)>::value_type;
  return [&]<template <typename...> typename Tuple, typename... Args,
             std::size_t... Is>(Tuple<Args...> const &,
                                std::integer_sequence<std::size_t, Is...>) {
    return message<L, sc::undefined<sc::args<Args...>, char_t, s[Is]...>>{};
  }(T{}, std::make_integer_sequence<std::size_t, std::size(s)>{});
}

template <logging::level L, typename Msg> constexpr auto to_message(Msg msg) {
  if constexpr (requires { msg.args; }) {
    return to_message<L, decltype(msg.str), decltype(msg.args)>();
  } else {
    return to_message<L, Msg, stdx::tuple<>>();
  }
}
} // namespace

namespace poc::logging {
class LogHandler {
public:
  constexpr LogHandler() = default;

  template <::logging::level Level, typename FilenameStringType,
            typename LineNumberType, typename MsgType>
  auto log(FilenameStringType, LineNumberType, MsgType const& msg) -> void {
    logMessage<Level>(msg);
  }

private:
  template <::logging::level Level, typename Msg>
  inline auto logMessage(Msg msg) -> void {
    msg.apply([&]<typename StringType>(StringType, auto... args) {
      using Message = decltype(to_message<Level>(msg));
      std::array<std::uint32_t, sizeof...(args)+1> logBuffer = {catalog<Message>(), static_cast<std::uint32_t>(args)...};
      //dispatch_message<Level>(catalog<Message>(),static_cast<std::uint32_t>(args)...);

      std::for_each(std::begin(logBuffer), std::end(logBuffer), [&](auto& el) -> void {
        std::cout << el << std::endl;
      });
    });
  }
};

struct config {
  constexpr config() = default;

  LogHandler logger{};
};

} // namespace poc::logging

template <>
inline auto logging::config<> = poc::logging::config{};
