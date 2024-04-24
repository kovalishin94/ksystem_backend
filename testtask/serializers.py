from rest_framework import serializers


class StatusSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=('open', 'close'))
    value = serializers.IntegerField(min_value=0, max_value=86399)


class DaySerializer(serializers.Serializer):
    monday = StatusSerializer(many=True)
    tuesday = StatusSerializer(many=True)
    wednesday = StatusSerializer(many=True)
    thursday = StatusSerializer(many=True)
    friday = StatusSerializer(many=True)
    saturday = StatusSerializer(many=True)
    sunday = StatusSerializer(many=True)

    def validate(self, data):
        '''
        Check double statuses in schedule
        '''
        status_list = []
        for day, statuses in data.items():
            for status in statuses:
                status_list.append(status.get('type'))

        for i in range(len(status_list)):
            if status_list[i-1] == status_list[i]:
                raise serializers.ValidationError(
                    f'Schedule Error! Double {status_list[i]} status')

        return data
