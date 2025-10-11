use std::io;
use std::str::FromStr;
use tracing_appender::rolling::{RollingFileAppender, Rotation};
use tracing_subscriber::{EnvFilter, fmt, layer::SubscriberExt, util::SubscriberInitExt};

pub fn setup_logger(
    log_level: &str,
    log_dir: &str,
    log_filename: &str,
) -> tracing_appender::non_blocking::WorkerGuard {
    // logger formatter
    let formatter = fmt::format()
        .compact()
        .with_level(true)
        .with_target(true)
        .with_file(true)
        .with_line_number(true);
    // logger filter
    let level = tracing::Level::from_str(log_level).unwrap_or(tracing::Level::INFO);
    let filter_layer = EnvFilter::builder()
        .with_default_directive(level.into())
        .from_env_lossy();
    // console logger
    let console_layer = fmt::layer()
        .with_writer(io::stdout)
        .with_ansi(true)
        .event_format(formatter.clone());
    // file logger
    let file_appender = RollingFileAppender::new(Rotation::DAILY, log_dir, log_filename);
    let (non_blocking_file, _guard) = tracing_appender::non_blocking(file_appender);
    let file_layer = fmt::layer()
        .with_writer(non_blocking_file)
        .with_ansi(false)
        .event_format(formatter.clone());
    // register logger
    tracing_subscriber::registry()
        .with(filter_layer)
        .with(console_layer)
        .with(file_layer)
        .init();

    _guard
}
