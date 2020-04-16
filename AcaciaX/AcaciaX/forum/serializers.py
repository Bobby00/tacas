from rest_framework import serializers

from forum.models import Preference, Post


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ('value', 'pk')

    def create(self, validated_data):
        preference = Preference(
            user=self.context['request'].user,
            post=self.context['post'],
            value=validated_data['value'])
        preference.save()
        return preference

    def update(self, instance, validated_data):
        instance.value = validated_data['value']
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    preference = PreferenceSerializer(many=True)
    class Meta:
        model = Post
        fields = ('message', 'pk', 'updated_by', 'preference')

       
