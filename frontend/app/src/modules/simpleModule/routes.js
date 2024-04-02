import test from './components/test.vue';
import module from './Module.vue';

export default  {
    path: "/simple",
    component: module,
    children: [
        {
            path: "test",
            component: test
        }
    ]
}
