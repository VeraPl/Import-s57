# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImportS57
                                 A QGIS plugin
 This plugin opens s 57 map and import its vector layers
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-02-26
        copyright            : (C) 2024 by Vera_Pliushchikova
        email                : vera2014-2015@mail.ru
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ImportS57 class from file ImportS57.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .open_s57 import ImportS57
    return ImportS57(iface)
