Home Assistant |Chat Status|
=================================================================================

Open source home automation that puts local control and privacy first. Powered by a worldwide community of tinkerers and DIY enthusiasts. Perfect to run on a Raspberry Pi or a local server.

Check out `home-assistant.io <https://home-assistant.io>`__ for `a
demo <https://demo.home-assistant.io>`__, `installation instructions <https://home-assistant.io/getting-started/>`__,
`tutorials <https://home-assistant.io/getting-started/automation/>`__ and `documentation <https://home-assistant.io/docs/>`__.

|screenshot-states|

Featured integrations
---------------------

|screenshot-integrations|

The system is built using a modular approach so support for other devices or actions can be implemented easily. See also the `section on architecture <https://developers.home-assistant.io/docs/architecture_index/>`__ and the `section on creating your own
components <https://developers.home-assistant.io/docs/creating_component_index/>`__.

If you run into issues while using Home Assistant or during development
of a component, check the `Home Assistant help section <https://home-assistant.io/help/>`__ of our website for further help and information.

.. |Chat Status| image:: https://img.shields.io/discord/330944238910963714.svg
   :target: https://www.home-assistant.io/join-chat/
.. |screenshot-states| image:: https://raw.githubusercontent.com/home-assistant/core/master/docs/screenshots.png
   :target: https://demo.home-assistant.io
.. |screenshot-integrations| image:: https://raw.githubusercontent.com/home-assistant/core/dev/docs/screenshot-integrations.png
   :target: https://home-assistant.io/integrations/

Sveriges Radio integration
---------------------

This repository also includes the Sveriges Radio integration, which lets you stream music and podcasts from Sveriges Radio, as well as get access to local traffic information.

Set up: 

1. Follow the instructions above for installing home-assistant on your prefered plattform. Note that the integration is develop for running on a home-assistant container, and support is not provided for other installation methods and devices.

2. After starting home-assistant, go to Settings → Devices and services → Add integration and search for Sveriges Radio. After choosing the integration you will be asked to pick the area you want traffic information from from the drop down menu. After choosing your traffic area you can choose to connect the sensors to a area in your house, or you can leave it unconnect (recommended).

Using it:

Traffic information can be found in text format under the overview tab. Music and podcasts can be found under the media brower tab. Podcasts are stored in folders sorted by the program the produced them.
