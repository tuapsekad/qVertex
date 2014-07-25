# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QVertex
                                 A QGIS plugin
 автоматизация землеустройства
                             -------------------
        begin                : 2014-07-24
        copyright            : (C) 2014 by Филиппов Владислав
        email                : filippov70@gmail.com
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
    """Load QVertex class from file QVertex.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .q_vertex import QVertex
    return QVertex(iface)
