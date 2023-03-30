#Copyright 2023, Battelle Energy Alliance, LLC

import sys, os
import json
import stix2
import logging
from hashlib import sha256
from stix2 import Identity, ExtensionDefinition, MemoryStore
from stix2.serialization import STIXJSONEncoder
from genson import SchemaBuilder
import os
from uuid import uuid4


def gen_uuid(string):
    """
    Generates the ID field for a stix object, using UUIDv4.
    param string -- type of the object to prepend to the uuid.

    """
    return f"{string}--{uuid4()}"


def hash_list(list_data):
    m = sha256()
    m.update("".join(sorted(list(set(list_data)))).encode())
    return str(m.hexdigest())


class StixLoader:
    """Class to manage creation, adding to and writing out our stix data."""

    def __init__(self, file_path=None, allow_custom=True):
        logging.debug("init")
        self.allow_custom = allow_custom
        self.create_bundle(file_path=file_path)

    def create_bundle(self, file_path=None):
        logging.info("creating bundle")
        self.ms = MemoryStore(allow_custom=self.allow_custom)
        self.ms_source = self.ms.source
        self.ms_sink = self.ms.sink
        if file_path is not None:
            self.ms.load_from_file(file_path)

    def stix_out(self, name=None):
        if not self.stix_loader:
            return None
        if name is None:
            logging.error("No name for STIX output.")
        else:
            path_name = f"{name}.json"
        self.sl.write_out(os.path.join(self.dir, path_name))

    def merge(self, items):
        logging.debug("Merging:")
        for item in items:
            logging.debug(f"Adding: {item}")
            self.ms_sink.add(item)

    def add_item(self, items):
        self.ms_sink.add(items, version=2.1)

    def get_sink_data(self):
        return self.ms.sink._data

    def write_out(self, path_):
        # We are not using the built in .save_to_file as its slow for some reason
        logging.debug(f"attempting to write_out to path: {path_}")
        logging.info("Starting save to file")
        # self.ms.save_to_file(path)
        d = {
            "type": "bundle",
            "id": gen_uuid("bundle"),
            "objects": [item for item in self.ms_source.query()],
        }

        if d["objects"]:
            logging.debug(d)
            logging.debug(path_)
            with open(path_, "w") as f:
                json.dump(d, f, cls=STIXJSONEncoder)
            logging.info(
                f"Finished save to file, number of objects: {len(list(self.ms_source.query()))}"
            )


class ExtensionFixer:
    def __init__(
        self, input_data=None, input_file=None, identity_name="INL", extensions={}
    ):
        self.data = input_data
        self.input_file = input_file
        self.identity_name = identity_name
        self.extensions = extensions
        self.output_objects = []
        # lookup val will be hashed sorted type key names.

    def run(self):
        if self.input_file is not None:
            with open(self.input_file) as f:
                data = json.load(f)
            data = self.pre_fix(data)
            self.data = stix2.parse(data, allow_custom=True)
        if self.data is not None:
            self.generate_groups()
            self.generate_extensions()
            self.replace_w_extensions()
            return self.output_objects
        else:
            raise Exception("No input data, cannot proceed")

    def pre_fix(self, data):
        if "type" in data and data["type"] == "bundle":
            for obj in data["objects"]:
                if "extensions" in obj and isinstance(obj["extensions"], dict):
                    to_del = []
                    for k, v in obj["extensions"].items():
                        if not isinstance(v, dict):
                            to_del.append(k)
                    for item in to_del:
                        del obj["extensions"][item]
                    if len(obj["extensions"]) == 0:
                        del obj["extensions"]
        return data

    def upsert_group(self, key, props):
        if key not in self.groups:
            builder = SchemaBuilder()
            builder.add_schema({"type": "object", "properties": {}})
            builder.add_object({k.lower(): v for k, v in props.items()})
            self.groups[key] = {"schema": builder, "props": props.keys()}
        else:
            self.groups[key]["schema"].add_object(
                {k.lower(): v for k, v in props.items()}
            )

    def generate_groups(self):
        self.groups = {}
        if isinstance(self.data, stix2.v21.bundle.Bundle):
            self.objects = self.data.objects
        elif isinstance(self.data, list):
            self.objects = self.data
        else:
            logging.critical("Parse data is not a list of STIX 2.1 bundle")
        for obj in self.objects:
            props = self.get_custom_props(obj)
            if props == {}:
                continue
            else:
                self.upsert_group(hash_list(sorted(props.keys())), props)

    def generate_extensions(self):
        self.identity = Identity(name=self.identity_name)
        self.output_objects.append(self.identity)

        for group_key, group_val in self.groups.items():
            ext_def = ExtensionDefinition(
                created_by_ref=self.identity,
                name=f"{self.identity_name}_{group_key}",
                extension_types=["property-extension"],
                # extension_properties=[prop.lower() for prop in group_val["props"]],
                version="1.0",
                schema=group_val["schema"].to_schema(),
                description="Autogenerated extension definition",
            )
            self.output_objects.append(ext_def)
            self.extensions[group_key] = {
                "ext": ext_def,
                "org_props": group_val["props"],
            }

    def replace_w_extensions(self):
        for obj in self.objects:
            key = self.obj_props_to_key(obj)
            if key is None:
                self.output_objects.append(obj)
                continue
            ext = self.extensions[key]["ext"]
            org_props = self.extensions[key]["org_props"]
            obj_dict = {k: v for k, v in obj.items()}
            extension_props = {}
            for prop in org_props:
                if prop in obj_dict:
                    extension_props[prop.lower()] = obj_dict[prop]
                    del obj_dict[prop]
            obj_dict["extensions"] = {
                ext.id: {"extension_type": ext.extension_types[0], **extension_props}
            }
            self.output_objects.append(stix2.parse(obj_dict))

    def get_custom_props(self, obj):
        if not obj.has_custom:
            return {}
        else:
            return {key: val for key, val in obj.items() if key not in obj._properties}

    def obj_props_to_key(self, obj):
        props = self.get_custom_props(obj)
        if props == {}:
            return None
        return hash_list(sorted(props.keys()))


def getextensionfixer():
    return es


if __name__ == "__main__":
    #Startup
    print('Extension Fixer...')
    if sys.argv[1] == "default":
        in_file_name = "../Examples/test1.json"
        out_file_name = "../Examples/testoutput.json"
        es = ExtensionFixer(input_file=in_file_name)
        fixed_stix = es.run()
        sl = StixLoader()
        sl.merge(fixed_stix)
        sl.write_out(out_file_name)
        print('# Extension Fixer...Done') 
        sys.exit()
    else:
        try:
            bundle_input = sys.argv[1]
            bundle_output = sys.argv[2]
            bundleCheck = sys.argv[3]
        except:        
            print('Argument Missing')
            sys.exit()
        if bundleCheck == "0":
            in_file_name = bundle_input
        else:
            in_file_name = bundle_output
        
        es = ExtensionFixer(input_file=in_file_name)
        fixed_stix = es.run()
        sl = StixLoader()
        sl.merge(fixed_stix)
        sl.write_out(bundle_output)

    print('Extension Fixer...Done') 

