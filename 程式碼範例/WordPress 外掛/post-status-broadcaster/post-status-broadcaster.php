<?php

/**
 * The plugin bootstrap file
 *
 * This file is read by WordPress to generate the plugin information in the plugin
 * admin area. This file also includes all of the dependencies used by the plugin,
 * registers the activation and deactivation functions, and defines a function
 * that starts the plugin.
 *
 * @link              https://netsowl.com/
 * @since             1.0.0
 * @package           Post_Status_Broadcaster
 *
 * @wordpress-plugin
 * Plugin Name:       WP 文章狀態廣播精靈
 * Plugin URI:        https://netsowl.com/
 * Description:       一個能在文章狀態有變化時發佈廣播通知特定網站的超實用 WordPress 外掛。
 * Version:           1.0.0
 * Author:            網梟軟體家
 * Author URI:        https://netsowl.com/
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       post-status-broadcaster
 * Domain Path:       /languages
 */

// If this file is called directly, abort.
if (!defined('WPINC')) {
	die;
}

/**
 * Currently plugin version.
 * Start at version 1.0.0 and use SemVer - https://semver.org
 * Rename this for your plugin and update it as you release new versions.
 */
define('POST_STATUS_BROADCASTER_VERSION', '1.0.0');

/**
 * The code that runs during plugin activation.
 * This action is documented in includes/class-post-status-broadcaster-activator.php
 */
function activate_post_status_broadcaster()
{
	require_once plugin_dir_path(__FILE__) . 'includes/class-post-status-broadcaster-activator.php';
	Post_Status_Broadcaster_Activator::activate();
}

/**
 * The code that runs during plugin deactivation.
 * This action is documented in includes/class-post-status-broadcaster-deactivator.php
 */
function deactivate_post_status_broadcaster()
{
	require_once plugin_dir_path(__FILE__) . 'includes/class-post-status-broadcaster-deactivator.php';
	Post_Status_Broadcaster_Deactivator::deactivate();
}

register_activation_hook(__FILE__, 'activate_post_status_broadcaster');
register_deactivation_hook(__FILE__, 'deactivate_post_status_broadcaster');

/**
 * The core plugin class that is used to define internationalization,
 * admin-specific hooks, and public-facing site hooks.
 */
require plugin_dir_path(__FILE__) . 'includes/class-post-status-broadcaster.php';

/**
 * Begins execution of the plugin.
 *
 * Since everything within the plugin is registered via hooks,
 * then kicking off the plugin from this point in the file does
 * not affect the page life cycle.
 *
 * @since    1.0.0
 */
function run_post_status_broadcaster()
{

	$plugin = new Post_Status_Broadcaster();
	$plugin->run();
}
run_post_status_broadcaster();
