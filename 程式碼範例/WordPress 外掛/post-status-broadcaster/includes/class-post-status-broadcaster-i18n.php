<?php

/**
 * Define the internationalization functionality
 *
 * Loads and defines the internationalization files for this plugin
 * so that it is ready for translation.
 *
 * @link       https://netsowl.com/
 * @since      1.0.0
 *
 * @package    Post_Status_Broadcaster
 * @subpackage Post_Status_Broadcaster/includes
 */

/**
 * Define the internationalization functionality.
 *
 * Loads and defines the internationalization files for this plugin
 * so that it is ready for translation.
 *
 * @since      1.0.0
 * @package    Post_Status_Broadcaster
 * @subpackage Post_Status_Broadcaster/includes
 * @author     網梟軟體家 <not provided>
 */
class Post_Status_Broadcaster_i18n {


	/**
	 * Load the plugin text domain for translation.
	 *
	 * @since    1.0.0
	 */
	public function load_plugin_textdomain() {

		load_plugin_textdomain(
			'post-status-broadcaster',
			false,
			dirname( dirname( plugin_basename( __FILE__ ) ) ) . '/languages/'
		);

	}



}
