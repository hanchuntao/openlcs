import json

from django.db import transaction

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.backoff_strategy import ProcedureException

from packages.mixins import PackageImportTransactionMixin

from packages.models import File
from packages.models import Source
from packages.models import Package
from packages.models import Path

from packages.serializers import BulkCreateFileSerializer
from packages.serializers import BulkPathSerializer
from packages.serializers import FileSerializer
from packages.serializers import PackageSerializer
from packages.serializers import PathSerializer
from packages.serializers import SourceSerializer


# Create your views here.
class FileViewSet(viewsets.ModelViewSet, PackageImportTransactionMixin):
    """
    API endpoint that allows files to be viewed or edited.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    bulk_create_file_serializer = BulkCreateFileSerializer

    def list(self, request, *args, **kwargs):
        """
        Get a list of files.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/files/  -H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            [
                {
                    "id": 1,
                    "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088aa"
                },
                {
                    "id": 2,
                    "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ab"
                },
                {
                    "id": 3,
                    "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac"
                },
                {
                    "id": 4,
                    "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ad"
                }
            ]

        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new file.

        ####__Request__####

            curl -X POST -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/files/ \
-d '{"swhid": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088cc"}' \
-H 'Authorization: Token your_token'

        ####__Response__####

            {
                "id": 5,
                "swhid": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088cc"
            }

            or

            {
                "swhid": ["file with this SWH ID already exists."]
            }
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific file.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/files/instance_pk/ -H 'Authorization: \
Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            {
                "id": 1,
                "swhid": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac"
            }
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update file from command line.

        ####__Request__####

            curl -X PATCH -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/files/instance_pk/ -d \
'{"swhid": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac"}' \
-H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
        """
        return super().update(request, *args, **kwargs)

    @action(methods=['POST', 'GET'], detail=False)
    def bulk_create_files(self, request, *args, **kwargs):
        """
        Bulk create files from command line.

        ####__Request__####

            curl -X POST -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/files/bulk_create_files/ -d \
'{"swhids": ["swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac", \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ad"]}' \
-H 'Authorization: Token your_token'

        ####__Response__####
            Success: HTTP 200 OK
            Error: HTTP 400 BAD REQUEST

        ####__JSON Response__####
            Success:

                {
                    "swhids":
                        {
                            \
'swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac',
                            \
'swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ad'
                        }
                }

                or

                {
                    "swhids":
                        {
                            \
'swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac'
                        }
                }

                or

                {"message":"No files created."}

            Error:

            {
                "message": {
                    "swhids": [
                        "Expected a list of items but got type \"str\"."
                    ]
                }
            }

            or

            {
                "message": [
                    "Error while bulk create files. Reason: duplicate key \
value violates unique constraint \"packages_file_swhid_key\"\\nDETAIL:  \
Key (swhid)=(swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ad) \
already exists.\\n"
                ]
            }

            or

            {
                "message": [
                    "Procedure request time out"
                ]
            }
        """
        data = request.data
        serializer = self.bulk_create_file_serializer(data=data)
        if serializer.is_valid():
            try:
                res_data = self.create_files(data.get('swhids'))
                return Response(data=res_data, status=status.HTTP_200_OK)
            except (RuntimeError, ProcedureException) as err:
                return Response(
                    data={'message': err.args},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data={'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


class SourceViewSet(viewsets.ModelViewSet, PackageImportTransactionMixin):
    """
    API endpoint that allows sources to be viewed or edited.
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    def list(self, request, *args, **kwargs):
        """
        Get a list of sources.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/sources/  -H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            [
                {
                    "id": 1,
                    "checksum": \
"72c9cfa91c6f417dc36053787f7ebd74791c0df8456554fdbaaab8e1aeb3c32d",
                    "name": "xsom-20110809svn.tar.gz",
                    "url": null,
                    "state": 0,
                    "archive_type": "rpm"
                },
                {
                    "id": 2,
                    "checksum": \
"1a07e3b8433a840f8eda2ba9300309c7023e92f9a053c01d777bf8f4a9c5e9fe",
                    "name": "xstring.tar.xz",
                    "url": null,
                    "state": 0,
                    "archive_type": "rpm"
                },
                {
                    "id": 3,
                    "checksum": \
"677fd81a6e8221e0d9064c9995373e180291f95d96d21920b994191154f51c9f",
                    "name": "xunicode.doc.tar.xz",
                    "url": null,
                    "state": 0,
                    "archive_type": "rpm"
                },
                {
                    "id": 4,
                    "checksum": \
"ba215daaa78c415fce11b9e58c365d03bb602eaa5ea916578d76861a468cc3d9",
                    "name": "xsetroot-1.1.1.tar.bz2",
                    "url": null,
                    "state": 0,
                    "archive_type": "rpm"
                }
            ]
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new source.

        ####__Request__####

            curl -X POST -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/sources/ \
-d '{"name": "xtab.doc.tar.xz", "checksum": \
"597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e", \
"archive_type": "rpm"}' \
-H 'Authorization: Token your_token'

        ####__Response__####
            Success: HTTP 200 OK

            Error:
                HTTP 400 BAD REQUEST,

                HTTP 500, Key (name, checksum)=(xtab.doc.tar.xz, \
597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e) \
already exists.

        ####__JSON Response__####
            Success:

                {
                    "id": 8,
                    "checksum": \
"597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e",
                    "name": "xtab.doc.tar.xz",
                    "url": null,
                    "state": 0,
                    "archive_type": "rpm"
                }

            Error:

                {"archive_type":["This field is required."]}

                Server Error (500)
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific source.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/sources/instance_pk/ -H 'Authorization: \
Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            {
                "id": 1,
                "checksum": \
"72c9cfa91c6f417dc36053787f7ebd74791c0df8456554fdbaaab8e1aeb3c32d",
                "name": "xsom-20110809svn.tar.gz",
                "url": null,
                "state": 0,
                "archive_type": "rpm"
            }
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update source from command line.

        ####__Request__####

            curl -X PATCH -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/sources/instance_pk/ -d \
'{"name": "xtab.doc.tar.xz", "checksum": \
"597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e", \
"archive_type": "rpm"}' \
-H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
        """
        return super().update(request, *args, **kwargs)


class PathViewSet(viewsets.ModelViewSet, PackageImportTransactionMixin):
    """
    API endpoint that allows Paths to be viewed or edited.
    """
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    bulk_path_serializer = BulkPathSerializer

    def list(self, request, *args, **kwargs):
        """
        Get a list of paths.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/paths/  -H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            [
                {
                    "id": 2,
                    "source": "yum.conf.fedora",
                    "file": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac",
                    "path": "/test1"
                },
                {
                    "id": 3,
                    "source": "zake-0.2.2.tar.gz",
                    "file": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088cc",
                    "path": "/test2"
                },
                {
                    "id": 4,
                    "source": "00001-rpath.patch",
                    "file": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088dd",
                    "path": "/test3"
                },
                {
                    "id": 5,
                    "source": "0000-Disable-network-based-unit-tests.patch",
                    "file": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ee",
                    "path": "/test4"
                }
            ]
"""
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new path.

        ####__Request__####

            curl -X POST -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/paths/ \
-d '{"file": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088aa", \
"source": "ab7cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3ss0b93cd652", \
"path": "/test5"}
-H 'Authorization: Token your_token'

        ####__Response__####

            Success: HTTP 200 OK
            Error: HTTP 400 BAD REQUEST

        ####__JSON Response__####

            Success:
                {
                  "id": 44496,
                  "source": \
"ab7cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3ss0b93cd652",
                  "file": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088aa",
                  "path": "/test5"
                }

            Error:

                Server Error (500)
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific path.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/paths/instance_pk/ -H 'Authorization: \
Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            {
                "id": 2,
                "source": "yum.conf.fedora",
                "file": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ac",
                "path": "/test1"
            }
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update path from command line.

        ####__Request__####

            curl -X PATCH -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/paths/instance_pk/ -d \
'{"file_id": 5, "source_id": 5, "path": "/test5"}' \
-H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
        """
        return super().update(request, *args, **kwargs)

    @action(methods=['POST', 'GET'], detail=False)
    def bulk_create_paths(self, request, *args, **kwargs):
        """
        Bulk create paths from command line.

        ####__Request__####

            curl -X POST -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/paths/bulk_create_paths/ -d \
'{"paths":[{"file": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088aa", \
"source": "ab7cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3ss0b93cd652", \
"path": "/test5"}, {"file": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ff", "source": \
"e01fb480caaa7c7963dcb3328a4700e631bef6070db0e8b685816d220e685f6c", \
"path": "/test6"}]}' \
-H 'Authorization: Token your_token'

        ####__Response__####
            Success: HTTP 200 OK
            Error: HTTP 400 BAD REQUEST

        ####__JSON Response__####
            Success:

                {
                    "paths": [
                        {
                            "id": 5,
                            "source": {
                                "id": 5,
                                "checksum": \
"597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd652",
                                "name": "xtab.doc.tar.xz",
                                "url": null,
                                "state": 0,
                                "archive_type": "rpm"
                            },
                            "file": {
                                "id": 5,
                                "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ee"
                            },
                            "path": "/test5"
                        },
                        {
                            "id": 6,
                            "source": {
                                "id": 6,
                                "checksum": \
"e01fb480caaa7c7963dcb3328a4700e631bef6070db0e8b685816d220e685f6c",
                                "name": "XStatic-Font-Awesome-4.7.0.0.tar.gz",
                                "url": null,
                                "state": 0,
                                "archive_type": "rpm"
                            },
                            "file": {
                                "id": 6,
                                "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ff"
                            },
                            "path": "/test6"
                        }
                    ]
                }

                or

                {
                    "paths": [
                        {
                            "id": 5,
                            "source": {
                                "id": 5,
                                "checksum": \
"597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd652",
                                "name": "xtab.doc.tar.xz",
                                "url": null,
                                "state": 0,
                                "archive_type": "rpm"
                            },
                            "file": {
                                "id": 5,
                                "swhid": \
"swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088ee"
                            },
                            "path": "/test5"
                        }
                    ]
                }

                or

                {"message": "No paths created."}

            Error:

               {
                   "message":[\
"Error while create paths. Reason: duplicate key \
value violates unique constraint \"packages_path_pkey\"\\nDETAIL: \
Key (id)=(5) already exists.\\n"]
                }

                or

               Server Error (500)
        """
        data = request.data
        serializer = self.bulk_path_serializer(data=data)
        if serializer.is_valid():
            try:
                res_data = self.create_paths(data.get("paths"))
                return Response(data=res_data, status=status.HTTP_200_OK)
            except (RuntimeError, ProcedureException) as err:
                return Response(
                    data={'message': err.args},
                    status=status.HTTP_400_BAD_REQUEST)


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Packages to be viewed or edited.
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def list(self, request, *args, **kwargs):
        """
        Get a list of packages.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/packages/  -H 'Authorization: Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            [
                {
                    "id": 2,
                    "source": \
"1a07e3b8433a840f8eda2ba9300309c7023e92f9a053c01d777bf8f4a9c5e9fe",
                    "nvr": "rhel7.0",
                    "sum_license": "",
                    "is_source": false
                },
                {
                    "id": 3,
                    "source": \
"677fd81a6e8221e0d9064c9995373e180291f95d96d21920b994191154f51c9f",
                    "nvr": "rhel9.0",
                    "sum_license": "",
                    "is_source": false
                },
                {
                    "id": 4,
                    "source": \
"ba215daaa78c415fce11b9e58c365d03bb602eaa5ea916578d76861a468cc3d9",
                    "nvr": "rhel6.0",
                    "sum_license": "",
                    "is_source": false
                },
                {
                    "id": 1,
                    "source": \
"72c9cfa91c6f417dc36053787f7ebd74791c0df8456554fdbaaab8e1aeb3c32d",
                    "nvr": "rhel8.0",
                    "sum_license": "",
                    "is_source": false
                }
            ]
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific package.

        ####__Request__####

            curl -X GET -H "Content-Type: application/json" \
%(HOST_NAME)s/%(API_PATH)s/packages/instance_pk/ -H 'Authorization: \
Token your_token'

        ####__Response__####

            HTTP 200 OK
            Content-Type: application/json
            {
                "id": 1,
                "source": \
"72c9cfa91c6f417dc36053787f7ebd74791c0df8456554fdbaaab8e1aeb3c32d",
                "nvr": "rhel8.0",
                "sum_license": "",
                "is_source": false
            }
        """
        return super().retrieve(request, *args, **kwargs)


class PackageImportTransactionView(APIView, PackageImportTransactionMixin):
    """
    Package import transaction

    data example:  # noqa
    {
        "swhids": [
            "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088aa",
            "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088bb"
        ],
        "source": {
            "name": "xtab.doc.tar.xz",
            "checksum": "597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e",
            "archive_type": "rpm"
        },
        "paths": [
            {
                "file": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088aa",
                "source": "597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e",
                "path": "/test5"
            },
            {
                "file": "swh:1:cnt:1fa0d32c021a24447540ab6dca496948de8088bb",
                "source": "597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e",
                "path": "/test6"
            }
        ],
        "package": {
            "source": "597cf23c7b32beaee76dc7ec42f6f04903a3d8239a4b820adf3a3350b93cd65e",
            "nvr": "rhel8.0",
            "sum_license": "",
            "is_source": false
        }
    }
    """
    def post(self, request, *args, **kwargs):
        try:
            file_path = request.data.get("file_path")
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return Response(
                data={'message': e.args},
                status=status.HTTP_400_BAD_REQUEST)

        swhids = data.get('swhids')
        source = data.get('source')
        paths = data.get('paths')
        package = data.get('package')
        if not any([swhids, source, paths, package]):
            return Response(
                data={'message': 'Not get enough data'},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                self.create_files(swhids)
                source, created = Source.objects.get_or_create(**source)
                # If source not exist in database, that's mean the paths
                # is not exist, bulk created them directly.
                if created:
                    self.create_paths(paths)
                    self.create_package(package)
            msg = f'Build {package.get("nvr")} imported successfully.'
            return Response(
                data={'message': msg},
                status=status.HTTP_200_OK)
        except (RuntimeError, ProcedureException) as err:
            return Response(
                data={'message': err.args},
                status=status.HTTP_400_BAD_REQUEST)