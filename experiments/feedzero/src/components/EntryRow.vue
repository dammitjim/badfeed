<template lang="pug">

    div(class="entry_row" :class="{ 'entry_row--detail': detailed, 'entry_row--important': important }")
        div(class="entry_row__body")
            span(class="entry_row__text")
                a(:href="entry.href") {{ entry.title }}
            ul(class="entry_row__actions")
                li(class="entry_row__actions__action")
                    a(href="#") Pin
                li(class="entry_row__actions__action")
                    a(href="#") Do
            span(class="entry_row__summary") {{ entry.summary }}
            div(class="entry_row__body__meta")
                span(class="entry_row__feed")
                    a(:href="entry.feed.href") {{ entry.feed.title }}
                span(class="entry_row__date") {{ entry.relativeDatePublished }}

</template>

<script lang="ts">
    import {Component, Prop, Vue} from 'vue-property-decorator';

    @Component
    export default class EntryRow extends Vue {
        @Prop() private entry: any;
        @Prop() private detailed!: boolean;
        @Prop() private important!: boolean;
    }
</script>

<style lang="stylus" scoped>
    .entry_row
        display flex
        height 50px
        align-items center
        justify-content center
        width 100%
        border 1px solid #C2C2C2
        border-bottom none
        padding 10px
        position relative

        &--detail
            height 100px

        &--important
            background-color #FFF9C4

        &:hover
            background-color darken(white, 1%)

            & ^[0]__actions
                display flex
                position absolute
                right 0

        &:last-child
        &:only-child
            border-bottom 1px solid #C2C2C2

        &__feed
            white-space nowrap
            overflow hidden
            text-overflow ellipsis
            padding-right 10px
            font-size var(--fz--supersub)

        &__text
            flex-grow 1
            white-space nowrap
            overflow hidden
            text-overflow ellipsis
            font-size $fz--sub
            font-weight 600

            a
                color $cl--med

        &__date
            flex-grow 0
            font-size var(--fz--supersub)

        &__body
            flex-grow 1
            display flex
            flex-direction column

            &__meta
                display flex
                flex-direction row
                align-items center

        &__actions
            display none
            list-style none
            margin-left 10px
            background white
            padding-left 20px

            &__action
                margin-right 20px

                &:hover
                    cursor pointer

        &__tertiary
            color black
</style>


