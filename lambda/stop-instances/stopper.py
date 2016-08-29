import boto3
import logging
import time

class Stopper:
  TAG_NAME = 'LambderStop'

  def __init__(self):
    self.ec2 = boto3.resource('ec2')
    logging.basicConfig()
    self.logger = logging.getLogger()

  def get_instances_to_stop(self):
    filters = [{'Name':'tag-key', 'Values': [self.TAG_NAME]}]
    instances = self.ec2.instances.filter(Filters=filters)
    return instances

  # Return the value of a specific tag on a resource
  # If the tag does not exist, return the value of 'default'
  def get_tag_value(self, resource, tag_name, default=None):
    tags = filter(lambda x: x['Key'] == tag_name, resource.tags)

    if not tags:
      return default

    return tags[0]['Value']

  def run(self):
    instances = self.get_instances_to_stop()

    for instance in instances:
      name     = self.get_tag_value(instance, 'Name', 'Unknown')
      name_str = name + " [{}]".format(instance.id)
      state    = instance.state['Name']

      if state == 'running':
        self.logger.info('Stopping ' + name_str)
        instance.stop()
        time.sleep(5)
      else:
        self.logger.info('Will not stop ' + name_str + ', state: ' + state)
